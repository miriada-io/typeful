import types
import typing

import pytest
from pytest import param

from type_cast import is_mapping


class MyClass:
    pass


@pytest.mark.parametrize(
    ["value", "collection_args", "expected"],
    [
        param({}, [], True),
        param({}, [int, int], True),
        param({}, [typing.Any, typing.Any], True),
        param({1: 1}, [typing.Any, typing.Any], True),
        param({"1": "1"}, [typing.Any, typing.Any], True),
        param({1: "1"}, [typing.Any, typing.Any], True),
        param({1: 1, 2: 2}, [typing.Any, typing.Any], True),
        param({"1": "1", "2": "2"}, [typing.Any, typing.Any], True),
        param({1: "1", "2": 2}, [typing.Any, typing.Any], True),
        param({1: 1, 2: 2}, [int, int], True),
        param({"1": "1", "2": "2"}, [int, int], False),
        param({1: "1", "2": 2}, [int, int], False),
        param({1: 1, 2: 2}, [str, str], False),
        param({"1": "1", "2": "2"}, [str, str], True),
        param({1: "1", "2": 2}, [str, str], False),
        param({1: 1, 2: 2}, [typing.Union[int, str], typing.Union[int, str]], True),
        param({"1": "1", "2": "2"}, [typing.Union[int, str], typing.Union[int, str]], True),
        param({1: "1", "2": 2}, [typing.Union[int, str], typing.Union[int, str]], True),
        param({1.2: "1", "2": 2.1}, [typing.Union[int, str], typing.Union[int, str]], False),
        param(tuple(), [], False),
        param([], [], False),
        param(object(), [], False),
        param(tuple, [], False),
        param(typing.Tuple, [], False),
        param(
            {None: [MyClass()], "123": [], "321": [MyClass(), MyClass()]}, [typing.Optional[str], list[MyClass]], True
        ),
        param({}, [int], TypeError("Mapping requires exactly 2 type args, got: ")),
        param({}, [int, str, bool], TypeError("Mapping requires exactly 2 type args, got: ")),
    ],
)
def test_is_mapping(
    value: typing.Any, collection_args: typing.Sequence[type | types.GenericAlias], expected: bool
) -> None:
    if isinstance(expected, Exception):
        with pytest.raises(type(expected), match=expected.args[0]):
            is_mapping(value, collection_args)
    else:
        assert is_mapping(value, collection_args) == expected
