import dataclasses
from collections.abc import Mapping
from typing import Any, TypeVar

from frozendict import frozendict
from no_value import NoValue
from typing_extensions import deprecated

from ._exceptions import FieldErrors
from .get_dataclass_field_name_to_field import get_dataclass_field_name_to_field
from .get_dataclass_field_name_to_type import get_dataclass_field_name_to_type
from .get_field_value import get_field_value
from .._type import DataclassProtocol, MaybeAnnotated, WideType, try_extract_type_notes

DP = TypeVar('DP', bound=DataclassProtocol)


def to_dataclass(
        value: Mapping[str, Any] | DP | object,
        dataclass_type: MaybeAnnotated[type[DP]],
        stop_on_first_error: bool = False
) -> DP:
    """
    Return a dataclass instance based on first argument:
        - dict will be used to initialize new dataclass instance
        - dataclass instance of same or child classes will be passed unchanged
        - any other object will be used to extract data by getattr

    Uses get_field_value to prepare data for dataclass initializer
    """
    dataclass_type: type[DP] = try_extract_type_notes(dataclass_type)[0]
    if not dataclasses.is_dataclass(dataclass_type):
        raise TypeError("expected dataclass type")

    if isinstance(value, dataclass_type):
        return value

    dataclass_kwargs: dict[str, Any] = {}
    field_name_to_field: frozendict[str, dataclasses.Field] = get_dataclass_field_name_to_field(dataclass_type)
    field_name_to_type: frozendict[str, WideType] = get_dataclass_field_name_to_type(dataclass_type)
    get_value = value.get if hasattr(value, "get") else lambda key, default: getattr(value, key, default)

    field_name_to_error: dict[str, Exception] = {}
    for field_name in field_name_to_field:
        field = field_name_to_field[field_name]
        field_type = field_name_to_type[field_name]
        raw_value = get_value(field_name, NoValue)
        try:
            result_value = get_field_value(
                type_=field_type, init=field.init, default=field.default,
                default_factory=field.default_factory, value=raw_value)
        except FieldErrors as e:
            field_name_to_error |= {f'{field_name}.{field}': error for field, error in e.field_to_error.items()}
            if stop_on_first_error:
                break
            continue
        except Exception as e:
            field_name_to_error[field_name] = e
            if stop_on_first_error:
                break
            continue

        if result_value is not NoValue:
            dataclass_kwargs[field_name] = result_value

    if field_name_to_error:
        raise FieldErrors(field_name_to_error)

    return dataclass_type(**dataclass_kwargs)


@deprecated("Use to_dataclass instead")
def dict_to_dataclass(
        dict_value: Mapping[str, Any] | DP | object, dataclass: MaybeAnnotated[type[DP]]
) -> DP:
    return to_dataclass(dict_value, dataclass)
