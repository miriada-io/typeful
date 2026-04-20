from typing import Annotated, TypeVar

import pytest
from pytest import param

from type_cast import try_extract_type_notes


def foo():
    pass


lambda_fun = lambda: 1  # noqa: E731 — intentional lambda for test coverage
T = TypeVar("T")
X = TypeVar("X")


@pytest.mark.parametrize(
    ["value", "expected", "notes"],
    [
        param(int, int, tuple()),
        param(Annotated[int, "test"], int, ("test",)),
        param(Annotated[int, "test", "ok"], int, ("test", "ok")),
        param(foo, foo, tuple()),
        param(Annotated[foo, "test"], foo, ("test",)),
        param(Annotated[lambda_fun, "test"], lambda_fun, ("test",)),
    ],
)
def test_try_extract_type_notes(value: T | Annotated[T, X], expected: T, notes: tuple[X, ...]) -> None:
    assert try_extract_type_notes(value) == (expected, notes)
