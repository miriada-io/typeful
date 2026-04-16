from typing import Any

import pytest

from type_cast import is_iterable


@pytest.mark.parametrize(['obj', 'result'], [
    ['test', False],
    [['test'], True],
    [[], True],
    [1, False],
    [set(), True],
    [{}, False],
    [{}.values(), True],
    [object(), False],
    [None, None],
], ids=repr)
def test_is_iterable(obj: Any, result: bool):
    assert is_iterable(obj) == result
