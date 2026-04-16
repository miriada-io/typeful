from typing import Any

from .str_to_bool import str_to_bool


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        return str_to_bool(value)
    raise TypeError(f'Attempt to convert {type(value).__qualname__} to bool: {value=}')
