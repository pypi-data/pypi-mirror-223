""" Base class for create a data unit that can be cached disk or in memory"""
import dataclasses
import logging
import pathlib
import pickle
import uuid
import zipfile
from os import PathLike
from typing import TypeVar, Generic, get_args

from . import fileio

log = logging.getLogger(__name__)

DATA = TypeVar("DATA")


@dataclasses.dataclass(kw_only=True)
class DataUnit(Generic[DATA]):
    """ A base class for a unit of data. The data will be generated on demands or cached.

    Subclass need to implement the function "generate_data()".
    """
    index: int
    name: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    __data__: DATA = dataclasses.field(default=None, compare=False)
    __file__: pathlib.Path | zipfile.Path = dataclasses.field(default=None, compare=False)

    def __init_subclass__(cls):
        cls.__data_type__ = get_args(cls.__orig_bases__[0])[0]

    def generate_data(self):
        raise NotImplementedError(f"{self.__class__.__name__} not fully implemented.")

    @property
    def data(self) -> DATA:
        """ generate the data or retrieve it from  memory if possible"""
        if self.__data__ is not None:
            return self.__data__
        elif self.__file__ is not None:
            return fileio.read(self.__file__, self.__data_type__)
        else:
            return self.generate_data()

    def is_cached(self) -> bool:
        """ Check if the data is either cached in memory or in a file"""
        return self.__data__ is not None or self.__file__ is not None

    def is_memory_cached(self) -> bool:
        """ Check if the data is cached in memory"""
        return self.__data__ is not None

    def is_file_cached(self) -> bool:
        """ Check if the data is cached in a file"""
        return self.__file__ is not None

    def cache_in_memory(self, reload=False):
        """ Cache the data in memory. The data will be either loaded from disk
        or generated. Is reload is False (default) and the data is already cached
        in memory, it won't be regenerated or reloaded from disk."""
        if reload:
            self.clear_memory_cache()
        self.__data__ = self.data

    def cache_in_file(self, file: PathLike[str], reload=False):
        """ Cache the data in a file. Is reload is False (default) and the data is
        already cached in memory, if will be loaded from memory and saved in file."""
        if reload:
            self.clear_memory_cache()
        file = pathlib.Path(file)
        file.parent.mkdir(parents=True, exist_ok=True)
        data = self.data
        with file.open("wb") as f:
            pickle.dump(data, f)
        self.__file__ = file

    def clear_memory_cache(self):
        """ Clear the memory cache so a next call to data will either load it from
        disk or generate it"""
        self.__data__ = None

    def copy(self, **changes):
        return dataclasses.replace(self, **changes)

    def __repr__(self) -> str:
        if self.is_cached():
            return f"{self.__class__.__name__}(cached in memory)"
        else:
            return f"{self.__class__.__name__}(not cached)"
