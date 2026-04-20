import types

import pytest
from pytest import param

from type_cast._type import get_non_generic_args


class Some:
    pass


@pytest.mark.parametrize(
    ["generic_alias", "expected"],
    [
        param(dict[int, Some | None], [int, Some, types.NoneType]),
        param(dict[int | str, list[Some | None] | set[Some]], [int, str, Some, types.NoneType, Some]),
        param(dict[int | str, list["Some | None"] | set["Some"]], [int, str, "Some | None", "Some"]),
    ],
)
def test_get_non_generic_args(generic_alias: types.GenericAlias, expected: list[type | str]):
    assert get_non_generic_args(generic_alias) == tuple(expected)
