import dataclasses
import datetime
import functools
import itertools
import json
import types
import typing
from collections.abc import Callable
from typing import Any, Union

from .._cast import to_bool, to_datetime
from .._type import MaybeAnnotated, WideType, get_container_type, is_instance, try_extract_type_notes

T = typing.TypeVar("T")


def pass_value(value: Any) -> Any:
    return value


@functools.cache
def get_converter(type_: MaybeAnnotated[type[T]]) -> Callable[[Any], T]:
    type_: WideType[T] = try_extract_type_notes(type_)[0]
    type_origin = typing.get_origin(type_)
    type_args = typing.get_args(type_)
    if not type_origin and isinstance(type_, type):
        if dataclasses.is_dataclass(type_):
            from .to_dataclass import to_dataclass

            return functools.partial(to_dataclass, dataclass_type=type_)
        converter = type_
        if type_ is bool:
            converter = to_bool
        if type_ is typing.Any:
            converter = pass_value
        if type_ is datetime.time:
            converter = datetime.time.fromisoformat
        if type_ is datetime.date:
            converter = datetime.date.fromisoformat
        if type_ is datetime.datetime:
            converter = to_datetime
    elif type_origin is Union or isinstance(type_, types.UnionType):

        def union_converter(value: str):
            if is_instance(value, type_args):
                return value
            for possible_type in type_args:
                try:
                    return get_converter(possible_type)(value)
                except (TypeError, ValueError, AttributeError):
                    pass
            raise ValueError(f"Expected one of: {type_args}, got {type(value)}: {value}")

        return union_converter
    elif type_origin is not None:
        container_type = get_container_type(type_origin)
        if container_type is dict:
            key_converter = get_converter(type_args[0])
            value_converter = get_converter(type_args[1])

            def converter(base_value: Any):
                raw_values = json.loads(base_value) if isinstance(base_value, str) else base_value
                if not isinstance(raw_values, dict):
                    raise ValueError(f"Expected dict, got {type(raw_values).__name__}: {raw_values}")
                parsed_values = [(key_converter(key), value_converter(value)) for key, value in raw_values.items()]
                result = container_type(parsed_values)
                return result
        elif container_type is tuple:
            has_ellipsis = False
            element_converters = []
            for type_ in type_args:
                if type_ is ...:
                    has_ellipsis = True
                else:
                    if has_ellipsis:
                        raise TypeError(
                            "Ellipsis (three dots (...)) should be the last in tuple to make it variable-length"
                        )
                    element_converters.append(get_converter(type_))
            if has_ellipsis:
                element_converters = itertools.cycle(element_converters)

            def converter(base_value: Any):
                raw_values = json.loads(base_value) if isinstance(base_value, str) else base_value
                if not isinstance(raw_values, (list, tuple, set, frozenset)):
                    raise ValueError(f"Expected iterable, got {type(raw_values).__name__}: {raw_values}")
                if not has_ellipsis and len(raw_values) != len(element_converters):
                    raise ValueError(f"Expected exactly {len(element_converters)} elements, got {len(raw_values)}")
                result = tuple(conv(val) for conv, val in zip(element_converters, raw_values, strict=False))
                return result
        else:
            element_converter = get_converter(type_args[0])

            def converter(base_value: Any):
                raw_values = json.loads(base_value) if isinstance(base_value, str) else base_value
                if not isinstance(raw_values, (list, tuple, set, frozenset)):
                    raise ValueError(f"Expected iterable, got {type(raw_values).__name__}: {raw_values}")
                parsed_values = [element_converter(element) for element in raw_values]
                result = container_type(parsed_values)
                return result
    elif isinstance(type_, dataclasses.InitVar):
        return get_converter(type_.type)
    else:
        raise TypeError(f"Attempt to cast to unexpected type: {type_} ({type(type_).__name__})")
    return converter
