import types
import typing

import pytest
from pytest import param

from type_cast import is_collection


@pytest.mark.parametrize(
    ["value", "collection_args", "expected"],
    [
        param([], [], True),
        param(tuple(), [], True),
        param(set(), [], True),
        param({1, 2, 3}, [int], True),
        param([1, 2, 3], [int], True),
        param((1, 2, 3), [int], True),
        param((1, "2", 3), [int], False),
        param([1, "2", 3], [int], False),
        param({1, "2", 3}, [int], False),
        param([1, "2", 3], [str], False),
        param([1, "2", 3], [typing.Union[str, int]], True),
        param([1, "2", 3.1], [typing.Union[str, int]], False),
        param([1, "2", 3.1], [typing.Any], True),
        param(object(), [], False),
        param(tuple, [], False),
        param(typing.Tuple, [], False),
        param({}, [int, bool], TypeError("Collection requires exactly 1 type arg, got:")),
    ],
)
def test_is_collection(
    value: typing.Any, collection_args: typing.Sequence[type | types.GenericAlias], expected: bool
) -> None:
    if isinstance(expected, Exception):
        with pytest.raises(type(expected), match=expected.args[0]):
            is_collection(value, collection_args)
    else:
        assert is_collection(value, collection_args) == expected
