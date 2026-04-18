import collections.abc
import types
from typing import Any, Iterable, Union, List, get_args, get_origin

from .get_container_type import get_container_type
from .is_mapping import is_mapping
from .is_collection import is_collection
from .is_tuple import is_tuple

_GENERIC_ALIAS_TYPES = (type(List[int]), type(list[int]))


def _always_iterable(obj, base_type=_GENERIC_ALIAS_TYPES):
    if obj is None:
        return iter(())
    if (base_type is not None) and isinstance(obj, base_type):
        return iter((obj,))
    try:
        return iter(obj)
    except TypeError:
        return iter((obj,))


def is_instance(
        val: Any,
        possible_types: type | types.GenericAlias | types.UnionType | Iterable[
                        type | types.GenericAlias | types.UnionType]
) -> bool:
    for type_ in _always_iterable(possible_types, base_type=_GENERIC_ALIAS_TYPES):
        if type_ == Any:
            return True

        type_origin = get_origin(type_)
        type_args = get_args(type_)
        if not type_origin and isinstance(type_, type):  # basic check
            if isinstance(val, type_):
                return True
        elif type_origin is Union or isinstance(type_, types.UnionType):
            if is_instance(val, type_args):
                return True
        else:
            container_type = get_container_type(type_origin)
            if container_type is None or not isinstance(val, container_type):
                continue

            if issubclass(container_type, collections.abc.Mapping):
                if is_mapping(val, type_args):
                    return True

            elif container_type is tuple:  # tuple has specific typing behaviour
                if is_tuple(val, type_args):
                    return True

            elif issubclass(container_type, collections.abc.Collection):
                if is_collection(val, type_args):
                    return True
    return False
