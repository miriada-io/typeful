from typing import Any

import pytest

from typeful import DEFAULT_BASE_TYPES, ClassInfo, to_list


@pytest.mark.parametrize(
    ["value", "base_type", "none", "expected"],
    [
        [[1, 2, 3], DEFAULT_BASE_TYPES, ..., [1, 2, 3]],
        [[], DEFAULT_BASE_TYPES, ..., []],
        [1, DEFAULT_BASE_TYPES, ..., [1]],
        [None, DEFAULT_BASE_TYPES, list, []],
        [None, DEFAULT_BASE_TYPES, None, None],
        [None, DEFAULT_BASE_TYPES, lambda: [None], [None]],
        ["foo", DEFAULT_BASE_TYPES, ..., ["foo"]],
        ["foo", None, ..., ["f", "o", "o"]],
        [{"f": 1}, DEFAULT_BASE_TYPES, ..., [{"f": 1}]],
        [{"f": 1}.keys(), DEFAULT_BASE_TYPES, ..., ["f"]],
    ],
    ids=repr,
)
def test_to_list(value: Any, base_type: ClassInfo, none, expected: tuple) -> None:
    assert to_list(value, base_type=base_type, none=none) == expected
