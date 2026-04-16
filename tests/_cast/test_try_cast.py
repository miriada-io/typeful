from typing import Any, Callable

import pytest
from pytest import param

from type_cast import try_cast


@pytest.mark.parametrize(['value', 'target_type', 'fallback_value', 'fallback_on', 'expected'], [
    param("123", int, None, Exception, 123),
    param("qwerty", int, None, Exception, None),
    param("qwerty", int, 'default', Exception, 'default'),
    param("qwerty", int, ..., TypeError, ValueError(r"invalid literal for int\(\) with base 10: 'qwerty'")),
])
def test_try_cast(
        value: Any,
        target_type: Callable[[Any], Any],
        fallback_value: Any | None,
        fallback_on: type[Exception],
        expected: Any | Exception
) -> Any:
    if isinstance(expected, Exception):
        with pytest.raises(type(expected), match=expected.args[0]):
            try_cast(value, target_type, fallback_value, fallback_on)
    else:
        assert try_cast(value, target_type, fallback_value, fallback_on) == expected
