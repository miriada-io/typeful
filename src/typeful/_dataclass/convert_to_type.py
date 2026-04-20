from typing import Any, TypeVar

from no_value import NoValue

from .._type import MaybeAnnotated, try_extract_type_notes
from ._exceptions import UnsupportedType
from .get_converter import get_converter

T = TypeVar("T")


def convert_to_type(type_: MaybeAnnotated[type[T]], value: Any | NoValue) -> T:
    # noinspection PyTypeChecker
    type_: type[T] = try_extract_type_notes(type_)[0]

    try:
        converter = get_converter(type_)
    except TypeError as e:
        raise UnsupportedType(repr(e)) from e

    value = converter(value)
    return value
