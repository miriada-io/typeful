from typing import TypeVar, Any, Callable

from .._type.is_iterable import is_iterable, ClassInfo, DEFAULT_BASE_TYPES

T = TypeVar('T', bound=Any)
P = TypeVar('P', bound=Any)


def to_tuple(
        x: T, base_type: ClassInfo | None = DEFAULT_BASE_TYPES, none: P | Callable[[], P] = tuple
) -> tuple[T, ...] | P:
    """If *obj* is iterable, convert to tuple::

        >>> to_tuple([1, 2, 3])
        (1, 2, 3)

    If *obj* is not iterable, wrap it in tuple::

        >>> to_tuple(1)
        (1,)

    If *obj* is ``None``, return *none*, by default empty tuple:

        >>> to_tuple(None)
        ()

    *none* could be set to literal or callable:

        >>> assert to_tuple(None, none=None) is None
        >>> to_tuple(None, none=lambda: (None, ))
        (None,)

    By default, binary and text strings, dicts, generic aliases are not considered iterable:

        >>> to_tuple('foo')
        ('foo',)

    If *base_type* is set, objects for which ``isinstance(obj, base_type)``
    returns ``True`` won't be considered iterable.

        >>> to_tuple([1, 2])  # list considered iterable by default
        (1, 2)
        >>> to_tuple([1, 2], base_type=(list,))  # Treat list as a unit
        ([1, 2],)

    Set *base_type* to ``None`` to avoid any special handling and treat objects
    Python considers iterable as iterable:

        >>> to_tuple('foo', base_type=None)
        ('f', 'o', 'o')

    Based on always_iterable from more_itertools==11.0.1
    """
    if x is None:
        return none() if callable(none) else none

    if isinstance(x, tuple):
        return x

    if is_iterable(x, base_type=base_type):
        return tuple(x)
    return (x, )
