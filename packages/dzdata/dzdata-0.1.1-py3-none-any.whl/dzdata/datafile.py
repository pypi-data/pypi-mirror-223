import contextlib
import fnmatch
import logging
import os
from os import PathLike
import pathlib
import re
import tempfile
import zipfile
from dataclasses import dataclass, field, fields, MISSING
from datetime import datetime
from types import UnionType
from typing import ClassVar, Any
from pathlib import Path
import os.path

from .field import file_entry, ATTR_FILE, DATA_TYPE, DATA_FILE
from . import fileio

log = logging.getLogger(__name__)


INFO_FILENAME = ".info"


def load(path: str | pathlib.Path):
    path = Path(path)
    if not path.exists() and (_path := Path(f"{path}.zip")).exists():
        path = _path
    return DzData.load(path)


# The list of registered datatype (datatype that can be loaded). Automatically
# populated when a class inherit from DzData.
__datafiles_subclasses__: dict = {}


class NotADzDataException(Exception):
    def __init__(self, file):
        self.file = file
        super().__init__(f"File {str(self.file)} is not a valid Datafiles.")


@dataclass(kw_only=True, repr=False)
class DzData:
    file: pathlib.Path | None = None

    # Saved in the datafiles
    info: dict = file_entry(None, filename=INFO_FILENAME)

    # not saved
    compress: ClassVar[bool | int] = True

    # data files info (not saved)
    __filename_list__: list[str] = field(default_factory=list)
    __name_dict__: dict[str, str] = field(default_factory=dict)

    @property
    def creation_time(self) -> str:
        return self.info["creation_time"]

    @property
    def datafiles_class(self) -> str:
        return self.info["datafiles_class"]

    def generate_datafiles_info(self):
        return {"creation_time": str(datetime.now()),
                "datafiles_class": self.__class__.__name__,
                "datafiles_version": "1.0.0"}

    def is_zip(self) -> bool:
        return self._is_zip(self.file)

    def __post_init__(self):
        if self.info is None:
            self.info = self.generate_datafiles_info()
        elif "datafiles_version" not in self.info:
            info = self.generate_datafiles_info()
            info.update(**self.info)
            self.info = info
        self.set_file(self.file)

    def set_file(self, file: str | pathlib.Path | None):
        if file is None:  # create a filename automatically
            self.file = self._get_next_filename_()
        else:
            self.file = Path(file)

    def __init_subclass__(cls, **kwargs):
        # Add the class as a datatype
        __datafiles_subclasses__[cls.__name__] = cls

    @classmethod
    def load(cls, file: PathLike):
        """ Load the DzData subclass from 'file'"""
        if cls._is_zip(file):
            with zipfile.ZipFile(file, "r") as zf:
                obj = cls._load(zf)
        else:
            obj = cls._load(file)

        if obj.datafiles_class != cls.__name__:
            # Was loaded using base class -> load using datafile_class
            if obj.datafiles_class not in __datafiles_subclasses__:
                raise NotImplementedError(f"The datafiles class {obj.datafile_class} don't exists.")
            obj = __datafiles_subclasses__[obj.datafiles_class].load(file)
        obj.set_file(file)
        return obj

    def write(self, file: str | pathlib.Path | zipfile.Path = None):
        """ Dump(create) the datafile. The file must not exist on disk. Only field that are
        not None will be written."""
        if self.file is None or file is not None:
            self.set_file(file)

        files = []
        if self.file.exists():
            log.error(f"Path {self.file} exists. Delete first if you want to recreate it.")
        elif self.is_zip():
            # Create a temporary directory to write the files to
            with tempfile.TemporaryDirectory() as tmp_dir:
                # write file to tmp dir
                self._write_in_path(Path(tmp_dir))

                # create zip and add files
                self.file.parent.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(self.file, "w", compression=self._zipfile_compression) as zf:
                    for file in pathlib.Path(tmp_dir).glob("**/*.*"):
                        files.append(os.path.relpath(file, tmp_dir))
                        zf.write(file, files[-1])
        else:
            (path := self.file).mkdir(parents=True)
            self._write_in_path(path)
            files = [os.path.relpath(file, path) for file in path.glob("**/*.*")]
        self._add_file_info(files)

    def add(self, data: str | dict[str, Any], value: Any = None, *, compress: bool | int = None):
        """ Add file to an existing datafiles. The data can be a dictionary of name: value to
        save multiple files in one write or a single file can be saved by setting a name in
        data and a value. The class compress value can be overwritten by setting 'compress'.
        """
        if not self.file.exists():
            raise ValueError(f"'{self.file}' doesn't exist. Use write() first.")
        if isinstance(data, dict):
            if value is not None:
                log.warning(f"Data as a dictionary was passed to add but 'value' is also set."
                            "The value parameter will be ignored.")
        elif isinstance(data, str):
            if value is None:
                raise ValueError(f"When adding a file 'value' must be set.")
            else:
                data = {data: value}
        else:
            raise ValueError(f"Wrong data format")
        if self.is_zip():
            with tempfile.TemporaryDirectory() as tmp_dir:
                for name, obj in data.items():
                    fileio.write(obj, name, root=tmp_dir)
                if compress is None:
                    compress = self.compress
                files = add_path_to_zip(self.file, tmp_dir, compression=compress)
        else:
            files = [os.path.relpath(fileio.write(obj, name, root=self.file), self.file)
                     for name, obj in data.items()]
        self._add_file_info(files)

    def _add_file_info(self, files: list[str]):
        self.__filename_list__.extend(files)
        for file in files:
            self.__name_dict__[os.path.splitext(file)[0]] = file

    def rescan(self):
        if self.is_zip():
            with zipfile.ZipFile(self.file) as zf:
                self.__filename_list__ = [i.filename for i in zf.infolist()]
                self.__name_dict__ = {os.path.splitext(file)[0]: file
                                      for file in self.__filename_list__}
        else:
            self.__filename_list__ = [os.path.relpath(p, self.file) for p in self.file.glob("**/*")]
            self.__name_dict__ = {os.path.splitext(f)[0]: f for f in self.__filename_list__}

    def get(self, *names, default=None):
        if not self.file.exists():
            raise ValueError(f"'{self.file}' doesn't exist. Use write() first.")
        if len(names) == 0:
            return
        field_type = {f.name: f.type for f in fields(self)}
        types = [field_type.get(name, None) for name in names]

        if self.is_zip():
            with zipfile.ZipFile(self.file, "r") as zf:
                root = zipfile.Path(zf)
                data = [self._get(n, t, root, default) for n, t in zip(names, types)]
        else:
            data = [self._get(n, t, self.file, default) for n, t in zip(names, types)]

        if len(names) > 1:
            return data
        else:
            return data[0]

    def _get(self, name, dtype, root, default):
        if (filename := self.__name_dict__.get(name, None)) is None:
            filename = name
        if filename not in self.__filename_list__:
            return default
        else:
            return fileio.read(filename, dtype, root=root)

    def get_path(self, name) -> zipfile.Path | pathlib.Path:
        if self.is_zip():
            return zipfile.Path(self.file, self.__name_dict__[name])
        else:
            return self.file / self.__name_dict__[name]

    @property
    def files(self) -> tuple:
        return tuple(self.__filename_list__)

    def __contains__(self, item):
        return item in self.__filename_list__ or item in self.__name_dict__

    def _get_next_filename_(self) -> Path:
        name = self.__class__.__name__
        files = list(Path().glob(f"{name}-*.zip"))
        if len(files) == 0:
            i = 1
        else:
            c = re.compile(name + r"-(\d+)\.zip")
            i = max([int(v) for v in re.findall(c, "\n".join((f.name for f in files)))]) + 1
        return Path(f"{name}-{i}.zip")

    def __repr__(self):
        if self.is_zip():
            return f"{self.__class__.__name__}(zipfile: {self.file})"
        else:
            return f"{self.__class__.__name__}(path: {self.file})"

    def glob(self, pattern: str) -> list[str]:
        return fnmatch.filter(self.__filename_list__, pattern)

    @contextlib.contextmanager
    def open_write_path(self,
                        compression: bool | int = None,
                        tmp_dir: str | os.PathLike[str] = None) -> pathlib.Path:
        """
        Context manager to append data to a temporary directory, and then add it to the zip file.

        Parameters:
        -----------
        compression : bool | int, optional
            Whether to compress the added data or not. If True, compression is enabled. If False,
            no compression is applied. If an integer, compression is enabled and the integer
            indicates the compression level (see zipfile module). Default is to self.compress.
        tmp_dir : str | PathLike[str], optional
            The path where the temporary directory will be create. The data will be stored in it
            before being added the zip file. If not provided, a system-generated temporary directory
             will be used.

        Returns:
        --------
        pathlib.Path
            The path to the temporary directory where the data is stored.
        """
        if self.is_zip():
            tmp = tempfile.TemporaryDirectory(dir=tmp_dir)
            path = pathlib.Path(tmp.name)
            try:
                yield path
            finally:
                if compression is None:
                    compression = self.compress
                self._add_file_info(add_path_to_zip(self.file, path, compression=compression))
                tmp.cleanup()
        else:
            try:
                yield self.file
            finally:
                self.rescan()

    @classmethod
    def _load(cls, root):
        """Load a datafiles from a root path or file. fileinfo is a diction
        Only fields set by either attribute() or file_entry() will be loaded from the file.

        Parameters
        ----------
        cls : dataclasses.dataclass
            The type of the dataclass to load.
        root : PathLike[str] | zipfile.ZipFile
            The directory of that datafiles or the opened zip file to load the dataclass from.

        Returns
        -------
        Any
            An instance of the dataclass loaded from the zip file.
        """
        if isinstance(root, zipfile.ZipFile):
            files = [i.filename for i in root.infolist()]
            root = zipfile.Path(root)
            name_dict = {os.path.splitext(file)[0]: file for file in files}
        else:
            files = Path(root).glob("**/*")
            name_dict = {os.path.splitext(os.path.relpath(file, root))[0]: file for file in files}

        if f"{INFO_FILENAME}" not in name_dict:
            raise NotADzDataException(root)

        data = {"__filename_list__": files, "__name_dict__": name_dict}
        attributes = fileio.read(name_dict[ATTR_FILE], root=root)

        for _field in fields(cls):
            # Get the name of the corresponding file entry, if any
            if (name := _field.metadata.get(DATA_FILE, None)) is not None:

                # Get the type of the field
                if (_type := _field.metadata.get(DATA_TYPE)) is MISSING:
                    # Need Python 3.10+
                    if type(_type := _field.type) == UnionType:
                        log.warning(f"The type of {_field.name} is not set and is an UnionType. "
                                    f"The type will be inferred from the extension. Set a "
                                    f"default value, default_factory or dtype if the final type is"
                                    f"wrong.")

                # Load the data from the corresponding file entry or attribute
                if name == ATTR_FILE:
                    data[_field.name] = attributes[_field.name]
                else:
                    if name == MISSING:
                        name = _field.name
                    if name in name_dict:
                        data[_field.name] = fileio.read(name_dict[name], _type, root=root)
                    elif name in files:
                        data[_field.name] = fileio.read(name, _type, root=root)
                    else:
                        pass

        # Create an instance of the dataclass with the loaded attributes
        return cls(**data)

    @staticmethod
    def _is_zip(file: PathLike) -> bool:
        return Path(file).suffix == ".zip"

    @property
    def _zipfile_compression(self):
        if not isinstance(self.compress, bool):
            return self.compress
        elif self.compress:
            return zipfile.ZIP_LZMA
        else:
            return zipfile.ZIP_STORED

    def _write_in_path(self, path: Path):
        attributes = {}
        for _field in fields(self):
            # Check if the field has a "zip" metadata attribute
            if (name := _field.metadata.get(DATA_FILE, None)) is not None:
                # Get the value of the field
                value = getattr(self, _field.name)
                if name == ATTR_FILE:
                    attributes[_field.name] = value
                elif value is not None:
                    if name == MISSING:
                        name = _field.name
                    if (dtype := _field.metadata.get(DATA_TYPE, MISSING)) is not MISSING:
                        fileio.write(value, name, path, dtype)
                    else:
                        fileio.write(value, name, path)

        # Write the attributes dictionary to a file in the temporary directory
        fileio.write(attributes, ATTR_FILE, path)


def add_path_to_zip(zip_file: str | PathLike[str],
                    path: str | PathLike[str],
                    compression: bool | int = True) -> list[str]:
    """
    Add all files in a path to a zip file.

    Parameters:
    -----------
    zip_file : str | PathLike[str]
        The path to the zip file to which the files will be added.
    path : str | PathLike[str]
        The path of the directory containing the files to be added.
    compression : bool | int, optional
        Whether to compress the added files or not. If True, compression is enabled. If False,
        no compression is applied. If an integer, compression is enabled and the integer
        indicates the compression level (see zipfile module). Default is True.

    Returns:
    --------
    list[str]
        The list of added file names.
    """
    files = []
    if isinstance(compression, bool):
        if compression:
            compression = zipfile.ZIP_LZMA
        else:
            compression = zipfile.ZIP_STORED
    with zipfile.ZipFile(zip_file, "a", compression=compression) as zf:
        for file in pathlib.Path(path).glob("**/*"):
            if file.is_file():
                files.append(os.path.relpath(file, path))
                zf.write(file, files[-1])
    return files
