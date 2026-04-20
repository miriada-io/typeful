import types
import typing

import pytest
from pytest import param

from type_cast import is_tuple


@pytest.mark.parametrize(
    ["value", "collection_args", "expected"],
    [
        param(tuple(), [], True),
        param(tuple(), [int], False),
        param(tuple(), [int, ...], True),
        param((1,), [], True),
        param((1,), [int], True),
        param((1,), [int, ...], True),
        param((1, 2), [], True),
        param((1, 2), [int], False),
        param((1, 2), [int, ...], True),
        param(("1",), [], True),
        param(("1",), [int], False),
        param(("1",), [int, ...], False),
        param(("1",), [typing.Any], True),
        param(("1", 2), [typing.Any], False),
        param(("1", 2), [typing.Any, typing.Any], True),
        param(("1", "2"), [], True),
        param(("1", "2"), [str], False),
        param(("1", "2"), [str, ...], True),
        param(("1", 2), [typing.Any, int], True),
        param(("1", 2), [str, typing.Any], True),
        param(("1", 2), [str, int], True),
        param(("1", 2), [str, int, ...], True),
        param(("1", 2), [str, ...], False),
        param(("1", 2, "1"), [str, int, ...], True),
        param(("1", 2, "1", "1"), [str, int, ...], False),
        param(("1", 2, "1", 2, "1"), [str, int, ...], True),
        param(("1", 2, "1", 2, "1"), [typing.Union[str, int], ...], True),
        param(("1", "1", 2, "1", 2), [typing.Union[str, int], ...], True),
        param({}, [], False),
        param([], [], False),
        param(object(), [], False),
        param(tuple, [], False),
        param(typing.Tuple, [], False),
        param(
            (1, 2),
            [..., int],
            TypeError(r"Ellipsis \(three dots \(...\)\) should be the last in tuple to make it variable-length"),
        ),
    ],
)
def test_is_tuple(
    value: typing.Any, collection_args: typing.Sequence[type | types.GenericAlias], expected: bool
) -> None:
    if isinstance(expected, Exception):
        with pytest.raises(type(expected), match=expected.args[0]):
            is_tuple(value, collection_args)
    else:
        assert is_tuple(value, collection_args) == expected
