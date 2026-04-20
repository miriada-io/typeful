from typing import Any

import pytest
from pytest import param

from type_cast import to_bool


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param(True, True),
        param(False, False),
        param(1, True),
        param(0, False),
        param(-1, True),
        param("yes", True),
        param("false", False),
        param("no", False),
        param([], TypeError("Attempt to convert list to bool")),
    ],
)
def test_to_bool(value: Any, expected: bool) -> None:
    if isinstance(expected, Exception):
        with pytest.raises(type(expected), match=expected.args[0]):
            to_bool(value)
    else:
        assert to_bool(value) == expected
