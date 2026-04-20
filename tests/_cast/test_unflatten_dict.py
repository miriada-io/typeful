from typing import Any

import pytest
from pytest import param

from typeful import unflatten_dict


@pytest.mark.parametrize(
    ["flatten_dict", "separator", "expected"],
    [
        param({}, ".", {}),
        param({"q": 1}, ".", {"q": 1}),
        param({"q.a": 1}, ".", {"q": {"a": 1}}),
        param({"q.a": 1, "q.b": 2}, ".", {"q": {"a": 1, "b": 2}}),
        param({"q.a": 1, "w.b": 2}, ".", {"q": {"a": 1}, "w": {"b": 2}}),
    ],
)
def test_unflatten_dict(flatten_dict: dict[str, Any], separator: str, expected: dict[str, Any | dict[str, Any]]):
    assert unflatten_dict(flatten_dict, separator) == expected
