import dataclasses
import functools
from typing import Any

from frozendict import frozendict


@functools.cache
def get_dataclass_field_name_to_field(
        dataclass_: Any,
        with_init_vars: bool = True, with_class_vars: bool = False
) -> frozendict[str, dataclasses.Field]:
    try:
        # noinspection PyUnresolvedReferences,PyProtectedMember
        fields = getattr(dataclass_, dataclasses._FIELDS)
    except AttributeError:
        raise TypeError("expected dataclass type")
    # noinspection PyUnresolvedReferences,PyProtectedMember
    allowed_field_types = {dataclasses._FIELD}
    # noinspection PyUnresolvedReferences,PyProtectedMember
    allowed_field_types |= {dataclasses._FIELD_INITVAR} if with_init_vars else set()
    # noinspection PyUnresolvedReferences,PyProtectedMember
    allowed_field_types |= {dataclasses._FIELD_CLASSVAR} if with_class_vars else set()
    # noinspection PyProtectedMember
    result = {name: field for name, field in fields.items() if field._field_type in allowed_field_types}
    return frozendict(result)
