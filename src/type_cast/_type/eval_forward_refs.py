import contextlib
import dataclasses
import inspect
import sys
import typing
from collections.abc import Mapping
from typing import Any

from frozendict import frozendict

from ._alias import WideType
from .dataclass_protocol import DataclassProtocol

if sys.version_info >= (3, 12):

    def eval_type(t, globalns, localns):
        # noinspection PyUnresolvedReferences,PyProtectedMember
        return typing._eval_type(t, globalns, localns, type_params=())
else:

    def eval_type(t, globalns, localns):
        # noinspection PyUnresolvedReferences,PyProtectedMember
        return typing._eval_type(t, globalns, localns)


@contextlib.contextmanager
def eval_forward_refs_in_local_dataclasses():
    yield
    current_frame = inspect.currentframe()
    contextmanager_frame = current_frame.f_back
    callee_frame = contextmanager_frame.f_back
    targets = [val for val in callee_frame.f_locals.values() if isinstance(val, DataclassProtocol)]
    _resolve_reverse_refs(*targets, localns=callee_frame.f_locals, globalns=callee_frame.f_globals)


def _resolve_reverse_refs(
    *targets: type[DataclassProtocol], localns: Mapping[str, Any], globalns: Mapping[str, Any]
) -> None:
    for target in targets:
        annotations = target.__annotations__
        for key, old_type in annotations.items():
            new_type = eval_type(old_type, globalns=globalns, localns=localns)
            if old_type != new_type:
                annotations[key] = new_type

        for f in dataclasses.fields(target):
            new_type = eval_type(f.type, globalns=globalns, localns=localns)
            if f.type != new_type:
                f.type = new_type


def get_evaled_dataclass_fields(obj: type[DataclassProtocol]) -> frozendict[str, WideType]:
    key_to_type = obj.__dict__.get("__key_to_type__")
    if key_to_type is None:
        # noinspection PyTypeChecker
        eval_dataclass_fields(obj)
        key_to_type = {f.name: f.type for f in dataclasses.fields(obj)}
        obj.__key_to_type__ = frozendict(key_to_type)
    return obj.__key_to_type__


def eval_dataclass_fields(obj: type[DataclassProtocol]) -> None:
    for base in reversed(obj.__mro__):
        base_globals = getattr(sys.modules.get(base.__module__, None), "__dict__", {})
        base_locals = dict(vars(base))
        if not isinstance(base, DataclassProtocol):
            continue
        fields = dataclasses.fields(base)
        for field in fields:
            value = field.type
            if value is None:
                value = type(None)
            if isinstance(value, str):
                value = typing.ForwardRef(value, is_argument=False, is_class=True)
            try:
                value = eval_type(value, base_globals, base_locals)
            except NameError as e:
                raise TypeError(
                    f"Failed to evaluate type {value!r}: not found referenced {e.name!r}. "
                    f"If it is class, created in local scope, wrap it in "
                    f"`with eval_forward_refs_in_local_dataclasses():` to evaluate type references in local scope "
                ) from None
            field.type = value
