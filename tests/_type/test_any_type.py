import typing
from typing import Any

import pytest
from pytest import param

from type_cast import AnyType


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param(0, False),
        param(42, False),
        param(-42, False),
        param(123.456, False),
        param("", False),
        param("qwe", False),
        param([], False),
        param([1], False),
        param({}, False),
        param(list, True),
        param(list[int], True),
        param(tuple, True),
        param(tuple[int, ...], True),
        param(tuple | dict, True),
        param(typing.Union[tuple, dict], True),
        param(typing.Annotated[list, "note"], True),
    ],
)
def test_isinstance_any_type(value: Any, expected: bool) -> None:
    assert isinstance(value, AnyType) == expected
