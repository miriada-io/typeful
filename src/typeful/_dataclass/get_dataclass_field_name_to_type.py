import functools
import typing

from frozendict import frozendict

from .._type import DataclassProtocol, WideType, get_evaled_dataclass_fields


@functools.cache
def get_dataclass_field_name_to_type(dataclass_: type[DataclassProtocol]) -> frozendict[str, WideType]:
    result: dict[str, WideType] = typing.get_type_hints(dataclass_)
    # noinspection PyTypeChecker
    return frozendict(result | get_evaled_dataclass_fields(dataclass_))
