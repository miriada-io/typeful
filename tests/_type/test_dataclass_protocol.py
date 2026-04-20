from dataclasses import dataclass
from typing import Any

import pytest
from pytest import param

from type_cast import DataclassProtocol


@dataclass
class DC:
    pass


class NonDC:
    pass


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param(DC(), True),
        param(DC, True),
        param(NonDC(), False),
        param(NonDC, False),
        param(17, False),
        param([], False),
    ],
)
def test_dataclass_protocol(value: Any, expected: bool) -> None:
    assert isinstance(value, DataclassProtocol) == expected
