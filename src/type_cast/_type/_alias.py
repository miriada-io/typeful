import types
import typing

note: typing.TypeAlias = typing.Annotated
TypingGenericAlias: typing.TypeAlias = type(typing.List[str])
AnnotatedAlias = type(typing.Annotated[int, ""])

T = typing.TypeVar("T")
MaybeAnnotated: typing.TypeAlias = T | typing.Annotated[T, typing.Any]
WideType: typing.TypeAlias = type | types.UnionType | types.GenericAlias | TypingGenericAlias  # OR typing.Annotated
AnyType: typing.TypeAlias = WideType | AnnotatedAlias
