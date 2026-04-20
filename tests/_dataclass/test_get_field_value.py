from dataclasses import MISSING, dataclass
from typing import Any, Callable

import pytest
from no_value import NoValue
from pytest import param

from typeful import FieldErrors, MissingField, WideType, get_field_value


@dataclass
class DCWithEmptyInit:
    pass


@dataclass
class DC:
    qqq: int


@pytest.mark.parametrize(
    ["type_", "init", "default", "default_factory", "value", "expected"],
    [
        param(..., False, ..., ..., ..., NoValue),
        param(int, True, ..., ..., "42", 42),
        param(..., True, MISSING, lambda: [], NoValue, NoValue),
        param(..., True, 42, MISSING, NoValue, NoValue),
        param(DCWithEmptyInit, True, MISSING, MISSING, NoValue, DCWithEmptyInit()),
        param(DC, True, MISSING, MISSING, NoValue, FieldErrors({"qqq": MissingField()})),
        param(int, True, MISSING, MISSING, NoValue, MissingField()),
    ],
)
def test_get_field_value(
    type_: WideType, init: bool, default: Any, default_factory: Callable, value: Any, expected: Any | Exception
):
    if isinstance(expected, Exception):
        with pytest.raises(type(expected)) as e:
            get_field_value(type_, init, default, default_factory, value)

        if isinstance(expected, FieldErrors):
            expected_field_name_to_error = expected.args[0]
            result_field_name_to_error = e.value.args[0]
            for name, expected_error in expected_field_name_to_error.items():
                assert name in result_field_name_to_error
                result_error = result_field_name_to_error[name]
                assert type(result_error) == type(expected_error), (
                    f"Expected {type(expected_error)} for {name=}, got {type(result_error)}"
                )
                assert result_error.args == expected_error.args, (
                    f"{expected_error.args=} for {name=}, got {result_error.args=}"
                )
            assert not (result_field_name_to_error.keys() - expected_field_name_to_error.keys())
    else:
        assert get_field_value(type_, init, default, default_factory, value) == expected
