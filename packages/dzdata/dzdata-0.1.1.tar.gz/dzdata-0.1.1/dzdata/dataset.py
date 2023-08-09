import dataclasses
from typing import Iterator, ClassVar, Generic, TypeVar, get_args
import logging

import dask.distributed
from dask.distributed import Client, LocalCluster
import pandas as pd
from pandas import DataFrame

from ticstat import TicStat

from . import DzData
from . import DataUnit
from . import fileio
from . import file_entry
from .utils import format_number

try:
    import ujson as json
except ImportError:
    import json


__DATA_PATH__ = "data"

log = logging.getLogger(__name__)

DATA = TypeVar("DATA", bound=DataUnit)


@dataclasses.dataclass
class Dataset(Generic[DATA], DzData):
    # metadata Will be converted to dataframe from list or dict if needed
    # metadata entry are used to build the data unit. The metadata can contain more information
    # than needed to build the data unit.
    metadata: DataFrame | list | dict = file_entry(default_factory=list, dtype=DataFrame)

    compress_data: bool | int = False

    # Set via the Generic
    __data_type__: ClassVar[DataUnit] = None
    __data_fields__: ClassVar[tuple] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__data_type__ = get_args(cls.__orig_bases__[0])[0]
        if cls.__data_type__ is DATA:
            # the generic type was not set and must be set by a child class
            pass
        else:
            cls.__data_fields__ = tuple(f.name for f in dataclasses.fields(cls.__data_type__))

    def __post_init__(self):
        super().__post_init__()

        if isinstance(self.metadata, list | dict):
            self.metadata = pd.DataFrame(self.metadata)
        elif not isinstance(self.metadata, pd.DataFrame):
            raise AttributeError("The metadata should be initialized with a dataframe a "
                                 "list or a dictionary.")
        if "name" not in self.metadata:
            self.metadata["name"] = [self.get_data_name(i) for i in range(len(self))]

    def __getitem__(self, item: int) -> DATA:
        params = self.metadata.loc[item, self.metadata.columns.isin(self.__data_fields__)]
        data = self.__data_type__(**params, index=item)
        if data.name in self:
            data.__file__ = self.get_path(data.name)
        return data

    def get_todo(self) -> list[DataUnit]:
        todo = [du for du in self if not du.is_cached()]
        if len(todo) == 0:
           log.debug("all data's file exists in the dataset.")
        else:
            log.debug(f"there is {len(todo)} / {len(self)} files missing in the dataset.")
        return todo

    def pre_generate_worker_thread_hook(self):
        pass

    def generate_data(self, client: int | dask.distributed.Client = None, batch_size=5000):
        if not self.file.exists():
            self.write()

        if len(todo := self.get_todo()) == 0:
            log.debug(f"All data for {self} already exist.")
        elif client is None:
            self._generate_data_single_thread(todo)
        elif isinstance(client, int):
            with Client(LocalCluster(n_workers=client, threads_per_worker=1)) as c:
                self._generate_data_dask(todo, c)
                c.shutdown()
        else:
            self._generate_data_dask(todo, client, batch_size)
        self.rescan()

    def _generate_data_single_thread(self, todo: list[DataUnit]):
        # single thread local
        with TicStat(len(todo), name=f"Generating {self}", printer=log.info) as ts:
            for du in todo:
                self.pre_generate_worker_thread_hook()
                data = du.data
                self.add({du.name: data}, compress=self.compress_data)
                ts.tic()

    def _generate_data_dask(self,
                            todo: list[DataUnit],
                            client: dask.distributed.Client,
                            batch_size: int = 5000
                            ):
        # generating with dask
        def func(du, path):
            self.pre_generate_worker_thread_hook()
            name = du.name
            data = du.data
            file = fileio.write(data, name, path)
            del data, du
            return name, file

        # Generate and save in bunch of 5000 to limit potential problems
        with TicStat(len(todo), name=f"Generating {self}", printer=log.info) as ts:
            N = 1500
            for i in range(int(len(todo) / N) + 1):
                with self.open_write_path(tmp_dir=".", compression=self.compress_data) as path:
                    futures = client.map(func, todo[i*N:(i+1)*N], path=path)
                    for future in dask.distributed.as_completed(futures):
                        name, file = future.result()
                        ts.tic({"name": name, "file": file})

    def get_data_name(self, index: int) -> str:
        return f"data/{format_number(index, len(self), zero_indexed=True)}"

    def __len__(self) -> int:
        return self.metadata.shape[0]

    def __iter__(self) -> Iterator:
        return (self[i] for i in range(len(self)))

    def __repr__(self):
        return f"{self.__class__.__name__}(file: {self.file}, " \
               f"generated data: {len(self.glob('data/*'))} / {len(self)}"
