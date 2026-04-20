import collections.abc
import types
from collections.abc import Sequence
from typing import Any


def is_mapping(value: Any, mapping_args: Sequence[type | types.GenericAlias]) -> bool:
    if not isinstance(value, collections.abc.Mapping):
        return False

    if not mapping_args:
        return True

    if len(mapping_args) != 2:
        raise TypeError(f"Mapping requires exactly 2 type args, got: {mapping_args}")

    key_type_list = [mapping_args[0]]
    value_type_list = [mapping_args[1]]

    from .is_instance import is_instance

    for key, val in value.items():
        if not is_instance(key, key_type_list) or not is_instance(val, value_type_list):
            return False
    return True
