import typing

from ._alias import MaybeAnnotated, WideType

Type = typing.TypeVar("Type", bound=WideType)


def try_extract_type_notes(value: MaybeAnnotated[Type]) -> tuple[Type, tuple]:
    if typing.get_origin(value) != typing.Annotated:
        return value, tuple()
    args = typing.get_args(value)
    return args[0], args[1:]
