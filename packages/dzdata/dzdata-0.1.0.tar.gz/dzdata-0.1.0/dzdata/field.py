import logging
from dataclasses import MISSING, Field, field
from typing import Any, Callable, Type

log = logging.getLogger(__name__)


DATA_FILE = "DATA_FILE"
DATA_TYPE = "DATA_TYPE"
ATTR_FILE = ".attributes"
INFO_FILE = ".info"


def file_entry(default: Any = MISSING,
               default_factory: Callable[[], Any] = MISSING,
               filename: str = MISSING,
               dtype: Type = MISSING,
               **kwargs
               ) -> Field:
    """
    Create a file entry for a ZipData file.

    Parameters
    ----------
    default : Any, optional
        Default value of the field (default is `MISSING`)
    default_factory : Callable[[], Any], optional
        Function that takes no arguments and returns the default value of the field.
        If specified, `default` parameter is ignored (default is `MISSING`)
    filename : str, optional
        Name of the file (without extension) to be associated with the field. If not set,
        the name of the field will be used (default is `MISSING`)
    dtype : Type, optional
        The type of the field. If not specified, the type will be inferred from the default
        value (default is `MISSING`)
    **kwargs:
        Additional keyword arguments to be passed to the `Field` constructor.

    Raises
    ------
    KeyError
        If the filename is set to the constant `ATTR_FILE` ('.attributes')
    ValueError
        If both `default` and `default_factory` parameters are specified.

    Returns
    -------
    field : Field
        The created field object with metadata indicating the filename.
    """
    if filename == ATTR_FILE:
        raise KeyError(f"{filename} cannot be use a a file name")
    return _create_zip_field(default=default, default_factory=default_factory, filename=filename,
                             dtype=dtype, **kwargs)


def attribute(default: Any = MISSING,
              default_factory: Callable[[], Any] = MISSING,
              dtype: Type = MISSING,
              **kwargs
              ) -> Field:
    """
    Create an attribute field for a ZipData file.

    The attributes are saved in a file named .attributes.yaml.

    Parameters
    ----------
    default : Any, optional
        The default value of the attribute (default is `MISSING`)
    default_factory : Callable[[], Any], optional
        Function that takes no arguments and returns the default value of the attribute.
        If specified, the `default` parameter is ignored (default is `MISSING`)
    dtype : Type, optional
        The type of the attribute. If not specified, the type will be inferred from the default
        value (default is `MISSING`)
    **kwargs:
        Additional keyword arguments to be passed to the `Field` constructor.

    Raises
    ------
    ValueError
        If both `default` and `default_factory` parameters are specified.

    Returns
    -------
    field : Field
        The created field object with metadata indicating the attribute filename and type.
    """
    return _create_zip_field(default=default, default_factory=default_factory, filename=ATTR_FILE,
                             dtype=dtype, **kwargs)


def _create_zip_field(default: Any = MISSING,
                      default_factory: Callable[[], Any] = MISSING,
                      filename: str = MISSING,
                      dtype: Type = MISSING,
                      **kwargs
                      ) -> Field:
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError('cannot specify both default and default_factory')
    if dtype is MISSING and default is not MISSING and default is not None:
        dtype = type(default)
    elif dtype is MISSING and default_factory is not MISSING:
        dtype = type(default_factory())
    # noinspection PyArgumentList
    return field(default=default,
                 default_factory=default_factory,
                 metadata={DATA_FILE: filename, DATA_TYPE: dtype},
                 **kwargs)

