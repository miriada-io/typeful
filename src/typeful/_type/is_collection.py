import collections.abc
import types
from collections.abc import Sequence
from typing import Any


def is_collection(value: Any, collection_args: Sequence[type | types.GenericAlias]) -> bool:
    if not isinstance(value, collections.abc.Collection):
        return False

    if not collection_args:
        return True

    if len(collection_args) != 1:
        raise TypeError(f"Collection requires exactly 1 type arg, got: {collection_args}")

    collection_type_list = [collection_args[0]]

    from .is_instance import is_instance

    for val in value:
        if not is_instance(val, collection_type_list):
            return False
    return True
