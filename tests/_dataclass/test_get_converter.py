import dataclasses
import datetime
import typing

import pytest
from pytest import param

from type_cast import get_converter, WideType

get_converter = get_converter.__wrapped__


@dataclasses.dataclass
class DC:
    ok: str


@pytest.mark.parametrize(['type_', 'value', 'expected'], [
    param(str, 'test', 'test'),
    param(int, '123', 123),
    param(bool, '+', True),
    param(datetime.time, '12:34', datetime.time(hour=12, minute=34)),
    param(datetime.date, '2026-04-07', datetime.date(year=2026, month=4, day=7)),
    param(datetime.datetime, '2026-04-07 12:34', datetime.datetime(year=2026, month=4, day=7, hour=12, minute=34)),
    param(typing.Any, '+', '+'),
    param(typing.Any, 11, 11),
    param(typing.Any, [], []),
    param(typing.Any, ['qwe'], ['qwe']),

    param(typing.Tuple[int, ...], '[1, 2, 3]', (1, 2, 3)),
    param(typing.Tuple[str, ...], '[1, 2, 3]', ("1", "2", "3")),
    param(typing.List[int], '[1, 2, 3]', [1, 2, 3]),
    param(typing.Set[int], '[1, 2, 3, 3, 5]', {1, 2, 3, 5}),
    param(typing.Dict[int, bool], '{"1": "+", "2": "on", "3": "-"}', {1: True, 2: True, 3: False}),
    param(tuple[int], [1], (1,)),
    param(tuple[int], (1,), (1,)),
    param(tuple[str], (1,), ("1",)),
    param(tuple[int, str], [1, 2], (1, "2")),
    param(tuple[int, str], (1, 2), (1, "2")),
    param(tuple[int, str], '[1, 2]', (1, "2")),
    param(tuple[int, int], [1, 2], (1, 2)),
    param(tuple[int, int], (1, 2), (1, 2)),
    param(tuple[int, int], '[1, 2]', (1, 2)),
    param(tuple[int, ...], '[1, 2, 3]', (1, 2, 3)),
    param(tuple[str, ...], '[1, 2, 3]', ("1", "2", "3")),
    param(list[int], '[1, 2, 3]', [1, 2, 3]),
    param(set[int], '[1, 2, 3, 3, 5]', {1, 2, 3, 5}),
    param(dict[int, bool], '{"1": "+", "2": "on", "3": "-"}', {1: True, 2: True, 3: False}),
    param(frozenset[int], '[1, 2, 3, 3, 5]', frozenset({1, 2, 3, 5})),

    param(typing.Union[int, float, bool], 'False', False),
    param(int | float | bool, 'False',  False),
    param(typing.Union[bool, int, float], 42, 42),
    param(bool | int | float, 42, 42),
    param(typing.Union[bool, DC], {"ok": "y"}, DC("y")),
    param(bool | DC, {"ok": "y"}, DC("y")),
    param(typing.List[typing.Union[bool, DC]], [{"ok": "y"}, 'false'], [DC("y"), False]),
    param(list[bool | DC], [{"ok": "y"}, 'false'], [DC("y"), False]),

    param(typing.Optional[list[int]], '[1,2]', [1, 2]),
    param(typing.Optional[int], '1', 1),
    param(typing.Union[int, float], '1.2', 1.2),
    param(int | float, '1.2', 1.2),

    param(typing.Dict[str, typing.List[int]], '{"a": [], "b": [2, 3]}', {"a": [], "b": [2, 3]}),
    param(dict[str, list[int]], '{"a": [], "b": [2, 3]}', {"a": [], "b": [2, 3]}),
])
def test_get_converter(type_: WideType, value: typing.Any, expected: typing.Any) -> None:
    assert get_converter(type_)(value) == expected
