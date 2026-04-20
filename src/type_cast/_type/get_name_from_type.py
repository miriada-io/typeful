import dataclasses
import types
import typing
from types import NoneType, UnionType
from typing import Union


def get_name_from_type(type_: type | types.UnionType | dataclasses.InitVar | None | NoneType) -> str:
    """
    Returns compact and unambiguous name of any basic or generic type
    >>> get_name_from_type(str)
    'str'
    >>> get_name_from_type(int)
    'int'
    >>> get_name_from_type(None)
    'None'
    >>> get_name_from_type(bool)
    'bool'
    >>> get_name_from_type(float)
    'float'
    >>> get_name_from_type(list)
    'list'
    >>> get_name_from_type(typing.List)
    'list'
    >>> get_name_from_type(list[int])
    'list[int]'
    >>> get_name_from_type(typing.List[int])
    'list[int]'
    >>> get_name_from_type(tuple)
    'tuple'
    >>> get_name_from_type(typing.Tuple)
    'tuple'
    >>> get_name_from_type(tuple[int])
    'tuple[int]'
    >>> get_name_from_type(typing.Tuple[int])
    'tuple[int]'
    >>> get_name_from_type(tuple[int, str])
    'tuple[int, str]'
    >>> get_name_from_type(typing.Tuple[int, str])
    'tuple[int, str]'
    >>> get_name_from_type(tuple[int, ...])
    'tuple[int, ...]'
    >>> get_name_from_type(typing.Tuple[int, ...])
    'tuple[int, ...]'
    >>> get_name_from_type(dict)
    'dict'
    >>> get_name_from_type(typing.Dict)
    'dict'
    >>> get_name_from_type(dict[str, int])
    'dict[str, int]'
    >>> get_name_from_type(typing.Dict[str, int])
    'dict[str, int]'
    >>> # noinspection PyTypeChecker
    >>> get_name_from_type(typing.Union)
    'Union'
    >>> get_name_from_type(typing.Union[str, int])
    'str | int'
    >>> get_name_from_type(str | int)
    'str | int'
    >>> get_name_from_type(typing.Optional[str])
    'str | None'
    >>> get_name_from_type(typing.Union[str, None])
    'str | None'
    >>> get_name_from_type(str | None)
    'str | None'
    >>> get_name_from_type(dataclasses.InitVar[bool])
    'bool'
    >>> get_name_from_type(dataclasses.InitVar[float])
    'float'
    >>> get_name_from_type(typing.Dict[typing.Tuple[typing.Union[int, str], ...], typing.Optional[list[str]]])
    'dict[tuple[int | str, ...], list[str] | None]'
    """

    type_origin = typing.get_origin(type_)
    type_args = typing.get_args(type_)
    if type_origin is not None and type_args is not None:
        if type_origin in (Union, UnionType):
            return " | ".join(list(get_name_from_type(sub_type) for sub_type in type_args))
        result = get_name_from_type(type_origin)
        if type_args:
            result += "[" + (", ".join(list(get_name_from_type(sub_type) for sub_type in type_args))) + "]"
        return result
    elif isinstance(type_, dataclasses.InitVar):
        return get_name_from_type(type_.type)
    elif type_ in (None, NoneType):
        return "None"
    elif type_ is Ellipsis:
        return "..."
    return type_.__name__
