import types
import typing

import pytest
from pytest import param

from type_cast import is_instance


@pytest.mark.parametrize(["val", "possible_types", "expected"], [
    param(1, [int], True),
    param(1, int, True),
    param(1, [str], False),
    param(1, str, False),
    param(1, [int, str], True),
    param(1, int | str, True),
    param(1, [str, int], True),
    param(1, str | int, True),
    param(('1', 1), [typing.Tuple[str, int]], True),
    param(('1', 1), typing.Tuple[str, int], True),
    param((1, '1'), [typing.Tuple[int, str]], True),
    param((1, '1'), typing.Tuple[int, str], True),
    param((1,), [typing.Tuple[str, int]], False),
    param((1,), typing.Tuple[str, int], False),
    param((1,), [typing.Tuple[int, str]], False),
    param((1,), typing.Tuple[int, str], False),
    param((1,), [typing.Tuple[int]], True),
    param((1,), typing.Tuple[int], True),
    param((1,), [typing.Tuple[str]], False),
    param((1,), typing.Tuple[str], False),
    param({"q": 1, "w": 2}, [dict[str, int], list[float]], True),
    param({"q": 1, "w": 2}, dict[str, int] | list[float], True),
    param({"q": 1, "w": 2.2}, [dict[str, int], list[float]], False),
    param({"q": 1, "w": 2.2}, dict[str, int] | list[float], False),
    param([1.1, 2.2], [dict[str, int], list[float]], True),
    param([1.1, 2.2], dict[str, int] | list[float], True),
    param({"q": 1, "w": "e"}, [dict[str, int | str]], True),
    param({"q": 1, "w": "e"}, dict[str, int | str], True),
    param(1.5, [lambda x: int(round(x))], False),
    param(1.5, [lambda x: int(round(x)), float], True),
], ids=repr)
def test_is_instance(
        val: typing.Any,
        possible_types: type | types.GenericAlias | types.UnionType | typing.Iterable[
                        type | types.GenericAlias | types.UnionType],
        expected: bool,
):
    assert is_instance(val, possible_types) is expected
