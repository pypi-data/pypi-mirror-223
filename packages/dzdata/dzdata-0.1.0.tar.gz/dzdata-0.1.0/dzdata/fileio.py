import os
import pathlib
import pickle
import zipfile
from typing import Any, TypeVar, Generic, get_args
from typing import IO

import pandas as pd
import yaml


def write(obj: Any,
          name: str | pathlib.Path,
          root: str | pathlib.Path | zipfile.Path = None,
          kind=None):
    if kind is None:
        kind = type(obj)
    return FileReaderWriterBase.find_reader_writer(kind).write(obj, name, root)


def read(file: str | pathlib.Path,
         kind: Any = None,
         root: str | pathlib.Path | zipfile.Path = None):

    if kind is None:
        kind = os.path.splitext(str(file))[-1]  # compatibility with zipfile.Path < 3.11

    if isinstance(root, str):
        root = pathlib.Path(root)

    return FileReaderWriterBase.find_reader_writer(kind).read(file, root=root)


T = TypeVar("T")


class FileReaderWriterBase(Generic[T]):
    extensions: list[str] = []
    __extensions_dict__: dict = {}
    __class_dict__: dict = {}

    def __init_subclass__(cls, **kwargs):
        for ext in cls.extensions:
            FileReaderWriterBase.__extensions_dict__[ext] = cls
        kind = get_args(cls.__orig_bases__[0])[0]
        FileReaderWriterBase.__extensions_dict__[kind] = cls
        FileReaderWriterBase.__class_dict__[kind] = cls

    @staticmethod
    def find_reader_writer(info):
        klass = FileReaderWriterBase.__extensions_dict__.get(info, None)
        if klass is not None:
            return klass
        for _type, klass in reversed(FileReaderWriterBase.__class_dict__.items()):
            if issubclass(info, _type):
                return klass
        # Should not happen!
        raise TypeError("The requested type cannot be read/loaded!")

    @classmethod
    def read(cls, file: str | pathlib.Path, root: pathlib.Path | zipfile.Path = None) -> T:
        #if isinstance(file, str):
        #    file = pathlib.Path(file)

        if root is None:
            with file.open("rb") as f:
                return cls.read_io(f)
        else:
            with (root / file).open("rb") as f:
                return cls.read_io(f)

    @classmethod
    def write(cls, obj: T, name: str, root: str | pathlib.Path = None) -> pathlib.Path:
        file = make_proper_path(name, cls.extensions[0], root)
        with file.open("wb") as f:
            cls.write_io(obj, f)
        return file

    @staticmethod
    def read_io(f: IO[bytes]):
        raise NotImplementedError(f"Reader not implemented.")

    @staticmethod
    def write_io(obj: Any, f: IO[bytes]):
        raise NotImplementedError(f"Writer not implemented.")

    def __repr__(self):
        return f"{self.__class__.__name__}"


def make_proper_path(name: str, ext: str = None, root: pathlib.Path | zipfile.Path = None):
    if root is None:
        root = pathlib.Path()
    elif isinstance(root, str):
        root = pathlib.Path(root)

    if ext is not None:
        _ext = os.path.splitext(str(name))[1]  # compatibility with zipfile.Path < 3.11
        if _ext != ext:
            name = f"{name}{ext}"

    file = root / name

    if isinstance(file, pathlib.Path):
        file.parent.mkdir(parents=True, exist_ok=True)
    return file


# ------------------- pickle ------------------- #
class PickleReaderWriter(FileReaderWriterBase[object]):
    extensions = [".pkl", ".pickle"]

    @staticmethod
    def read_io(f: IO[bytes]) -> Any:
        return pickle.load(f)

    @staticmethod
    def write_io(obj: Any, f: IO[bytes]):
        pickle.dump(obj, f)


# ------------------- dataframe ------------------- #
class DataFrameReaderWriter(FileReaderWriterBase[pd.DataFrame]):
    extensions = [".csv"]

    @staticmethod
    def read_io(f: IO[bytes]) -> pd.DataFrame:
        return pd.read_csv(f, index_col=0)

    @staticmethod
    def write_io(obj: pd.DataFrame, f: IO[bytes]):
        obj.to_csv(f)


# ------------------- dictionary ------------------- #

class DictionaryReaderWriter(FileReaderWriterBase[dict]):
    extensions = [".yaml", ".yml"]

    @staticmethod
    def read_io(f: IO[bytes]) -> dict:
        return yaml.safe_load(f.read().decode())

    @staticmethod
    def write_io(obj: dict, f: IO[bytes]):
        f.write(yaml.safe_dump(obj).encode())


# ------------------- string ------------------- #

class StringReaderWriter(FileReaderWriterBase[str]):
    extensions = [".txt"]

    @staticmethod
    def read_io(f: IO[bytes]) -> str:
        return f.read().decode()

    @staticmethod
    def write_io(obj: str, f: IO[bytes]):
        f.write(obj.encode())


# ------------------- list[str] ------------------- #

class StringListReaderWriter(FileReaderWriterBase[list]):
    """ Warning: The reader/writer is a bit dumb."""
    extensions = [".lst"]

    @staticmethod
    def read_io(f: IO[bytes]) -> list[str]:
        txt = f.read().decode()
        return txt.split("\n")

    @staticmethod
    def write_io(obj: str, f: IO[bytes]):
        f.write("\n".join(obj).encode())
