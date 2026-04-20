import dataclasses
from collections.abc import Callable
from typing import Any, TypeVar

from no_value import NoValue
from typing_extensions import deprecated

from .._type import MaybeAnnotated, WideType, try_extract_type_notes
from ._exceptions import MissingField
from .convert_to_type import convert_to_type

T = TypeVar("T")


def get_field_value(
    type_: MaybeAnnotated[type[T]],
    init: bool,
    default: Any,
    default_factory: Callable,
    value: Any,
) -> T:
    """
    Implement dataclass field logic init/default/default_factory.
    WARNING! with value == NoValue and is_dataclass(type_): will try to initialize type_ instance from empty dict
    (it's useful in cascade configs parsing)
    Uses convert_to_type to convert value.
    """
    if not init:
        return NoValue

    type_: WideType = try_extract_type_notes(type_)[0]
    if value != NoValue:
        return convert_to_type(type_, value)
    if default != dataclasses.MISSING:
        return NoValue
    if default_factory != dataclasses.MISSING:
        return NoValue

    # attempt to init dataclass
    if dataclasses.is_dataclass(type_):
        return convert_to_type(type_, {})

    raise MissingField()


@deprecated("Use get_field_value instead")
def convert(
    type_: MaybeAnnotated[type[T]],
    init: bool,
    default: Any,
    default_factory: Callable,
    value: Any,
) -> T:
    return get_field_value(type_=type_, init=init, default=default, default_factory=default_factory, value=value)
