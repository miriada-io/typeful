import types
import typing

ClassInfo: typing.TypeAlias = type | types.UnionType | tuple['ClassInfo', ...]
DEFAULT_BASE_TYPES: tuple[type, ...] = (str, bytes, dict, type(typing.List[int]), type(list[int]))


def is_iterable(obj: typing.Any, base_type: ClassInfo | None = DEFAULT_BASE_TYPES) -> bool | None:
    """If *obj* is iterable, return True::

        >>> is_iterable([1, 2, 3])
        True

    If *obj* is not iterable, return False::

        >>> is_iterable(1)
        False

    If *obj* is ``None``, return None:

        >>> assert is_iterable(None) is None

    By default, binary and text strings, dicts, generic aliases are not considered iterable:

        >>> is_iterable('foo')
        False

    If *base_type* is set, objects for which ``isinstance(obj, base_type)``
    returns ``True`` won't be considered iterable.

        >>> is_iterable([1, 2])  # list considered iterable by default
        True
        >>> is_iterable([1, 2], base_type=(list,))  # Treat list as a unit
        False

    Set *base_type* to ``None`` to avoid any special handling and treat objects
    Python considers iterable as iterable:

        >>> is_iterable('foo', base_type=None)
        True

    Based on always_iterable from more_itertools==11.0.1
    """
    if obj is None:
        return None

    if (base_type is not None) and isinstance(obj, base_type):
        return False

    try:
        iter(obj)
        return True
    except TypeError:
        return False
