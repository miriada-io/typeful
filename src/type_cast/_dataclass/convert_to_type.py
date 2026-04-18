from typing import TypeVar, Any

from no_value import NoValue

from ._exceptions import UnsupportedType
from .get_converter import get_converter
from .._type import MaybeAnnotated, try_extract_type_notes

T = TypeVar('T')


def convert_to_type(type_: MaybeAnnotated[type[T]], value: Any | NoValue) -> T:
    # noinspection PyTypeChecker
    type_: type[T] = try_extract_type_notes(type_)[0]

    try:
        converter = get_converter(type_)
    except TypeError as e:
        raise UnsupportedType(repr(e)) from e

    value = converter(value)
    return value
