import itertools
import types
from collections.abc import Iterable
from typing import Any


def is_tuple(value: Any, tuple_args: Iterable[type | types.GenericAlias]) -> bool:
    if not isinstance(value, tuple):
        return False

    has_ellipsis = False
    type_checks = []
    for inner_type in tuple_args:
        if inner_type is ...:
            has_ellipsis = True
        else:
            if has_ellipsis:
                raise TypeError("Ellipsis (three dots (...)) should be the last in tuple to make it variable-length")
            type_checks.append(inner_type)
    if has_ellipsis:
        type_checks = itertools.cycle(type_checks)
    elif type_checks:
        if len(type_checks) != len(value):
            return False

    from .is_instance import is_instance

    for val, inner_type in zip(value, type_checks, strict=False):
        if not is_instance(val, [inner_type]):
            return False

    return True
