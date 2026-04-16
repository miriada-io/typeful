import typing
from dataclasses import InitVar

import pytest
from pytest import param

from type_cast import get_name_from_type


@pytest.mark.parametrize(['type_', 'expected'], [
    param(str, 'str'),
    param(int, 'int'),
    param(None, 'None'),
    param(bool, 'bool'),
    param(float, 'float'),

    param(list, 'list'),
    param(typing.List, 'list'),
    param(list[int], 'list[int]'),
    param(typing.List[int], 'list[int]'),

    param(tuple, 'tuple'),
    param(typing.Tuple, 'tuple'),
    param(tuple[int], 'tuple[int]'),
    param(typing.Tuple[int], 'tuple[int]'),
    param(tuple[int, str], 'tuple[int, str]'),
    param(typing.Tuple[int, str], 'tuple[int, str]'),
    param(tuple[int, ...], 'tuple[int, ...]'),
    param(typing.Tuple[int, ...], 'tuple[int, ...]'),

    param(dict, 'dict'),
    param(typing.Dict, 'dict'),
    param(dict[str, int], 'dict[str, int]'),
    param(typing.Dict[str, int], 'dict[str, int]'),

    param(typing.Union, 'Union'),
    param(typing.Union[str, int], 'str | int'),
    param(str | int, 'str | int'),

    param(typing.Optional[str], 'str | None'),
    param(typing.Union[str, None], 'str | None'),
    param(str | None, 'str | None'),

    param(InitVar[bool], 'bool'),
    param(InitVar[float], 'float'),

    param(
        typing.Dict[typing.Tuple[typing.Union[int, str], ...], typing.Optional[list[str]]],
        'dict[tuple[int | str, ...], list[str] | None]'
    ),
])
def test_get_name_from_type(type_: type, expected: str) -> None:
    assert get_name_from_type(type_) == expected
