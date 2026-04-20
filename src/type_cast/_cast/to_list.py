from collections.abc import Callable
from typing import Any, TypeVar

from .._type.is_iterable import DEFAULT_BASE_TYPES, ClassInfo, is_iterable

T = TypeVar("T", bound=Any)
P = TypeVar("P", bound=Any)


def to_list(x: T, base_type: ClassInfo | None = DEFAULT_BASE_TYPES, none: P | Callable[[], P] = list) -> list[T] | P:
    """If *obj* is iterable, convert to list::

        >>> to_list((1, 2, 3))
        [1, 2, 3]

    If *obj* is not iterable, wrap it in list::

        >>> to_list(1)
        [1]

    If *obj* is ``None``, return *none*, by default empty list:

        >>> to_list(None)
        []

    *none* could be set to literal or callable:

        >>> assert to_list(None, none=None) is None
        >>> to_list(None, none=lambda: [None])
        [None]

    By default, binary and text strings, dicts, generic aliases are not considered iterable:

        >>> to_list('foo')
        ['foo']

    If *base_type* is set, objects for which ``isinstance(obj, base_type)``
    returns ``True`` won't be considered iterable.

        >>> to_list((1, 2))  # tuple considered iterable by default
        [1, 2]
        >>> to_list((1, 2), base_type=(tuple,))  # Treat tuple as a unit
        [(1, 2)]

    Set *base_type* to ``None`` to avoid any special handling and treat objects
    Python considers iterable as iterable:

        >>> to_list('foo', base_type=None)
        ['f', 'o', 'o']

    Based on always_iterable from more_itertools==11.0.1
    """
    if x is None:
        return none() if callable(none) else none

    if isinstance(x, list):
        return x

    if is_iterable(x, base_type=base_type):
        return list(x)
    return [x]
