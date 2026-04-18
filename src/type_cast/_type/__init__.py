from ._alias import TypingGenericAlias, AnnotatedAlias, MaybeAnnotated, WideType, AnyType, note
from .dataclass_protocol import DataclassProtocol
from .eval_forward_refs import eval_forward_refs_in_local_dataclasses, eval_type
from .eval_forward_refs import get_evaled_dataclass_fields, eval_dataclass_fields
from .get_container_type import get_container_type
from .get_name_from_type import get_name_from_type
from .get_non_generic_args import get_non_generic_args
from .is_collection import is_collection
from .is_instance import is_instance
from .is_iterable import is_iterable, ClassInfo, DEFAULT_BASE_TYPES
from .is_mapping import is_mapping
from .is_tuple import is_tuple
from .try_extract_type_notes import try_extract_type_notes

__all__ = [
    "note",
    "AnyType",
    "WideType",
    "MaybeAnnotated",
    "DataclassProtocol",
    "eval_forward_refs_in_local_dataclasses",
    "get_evaled_dataclass_fields",
    "get_container_type",
    "get_name_from_type",
    "get_non_generic_args",
    "is_collection",
    "is_instance",
    "is_iterable",
    "is_mapping",
    "is_tuple",
    "try_extract_type_notes",
    "ClassInfo",
    "DEFAULT_BASE_TYPES",
]
