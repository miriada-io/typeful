import itertools
import types
import typing


def get_non_generic_args(generic_alias: types.GenericAlias) -> tuple[type, ...]:
    return tuple(itertools.chain.from_iterable(
        get_non_generic_args(arg) if isinstance(arg, types.GenericAlias | types.UnionType) else (arg, )
        for arg in typing.get_args(generic_alias)
    ))
