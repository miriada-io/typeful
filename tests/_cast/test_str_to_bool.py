import pytest
from pytest import param

from typeful import str_to_bool


@pytest.mark.parametrize(
    ["bool_str", "expected"],
    [
        param("true", True),
        param("1", True),
        param("on", True),
        param("+", True),
        param("yes", True),
        param("false", False),
        param("0", False),
        param("off", False),
        param("-", False),
        param("no", False),
        param("not sure", ValueError("invalid literal for boolean:")),
    ],
)
def test_str_to_bool__true(bool_str: str, expected: bool) -> None:
    if isinstance(expected, Exception):
        with pytest.raises(type(expected), match=expected.args[0]):
            str_to_bool(bool_str)
    else:
        assert str_to_bool(bool_str) == expected
