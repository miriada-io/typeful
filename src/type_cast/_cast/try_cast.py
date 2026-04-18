from typing import Any, TypeVar, Callable, overload

T = TypeVar('T')
F = TypeVar('F')


@overload
def try_cast(value: Any, target_type: Callable[[Any], T], fallback_value: None = None,
             fallback_on: type[Exception] = Exception) -> T | None: pass


@overload
def try_cast(value: Any, target_type: Callable[[Any], T], fallback_value: F,
             fallback_on: type[Exception] = Exception) -> T | F: pass


def try_cast(value: Any, target_type: Callable[[Any], T], fallback_value: F | None = None,
             fallback_on: type[Exception] = Exception) -> T | F | None:
    try:
        return target_type(value)
    except fallback_on:
        return fallback_value
