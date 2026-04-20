import datetime
from typing import Any

import pytest
from pytest import param

from typeful import to_datetime


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param(
            "2026-04-02T17:10:01.594503+03:00",
            datetime.datetime(
                year=2026,
                month=4,
                day=2,
                hour=17,
                minute=10,
                second=1,
                microsecond=594503,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=10800)),
            ),
        ),
        param(
            "2026-04-02T17:10:01.594503",
            datetime.datetime(year=2026, month=4, day=2, hour=17, minute=10, second=1, microsecond=594503),
        ),
        param(
            "2026-04-02 17:10:01.594503",
            datetime.datetime(year=2026, month=4, day=2, hour=17, minute=10, second=1, microsecond=594503),
        ),
        param("2026-04-02 17:10:01", datetime.datetime(year=2026, month=4, day=2, hour=17, minute=10, second=1)),
        param("2026-04-02 17:10", datetime.datetime(year=2026, month=4, day=2, hour=17, minute=10, second=0)),
        param("2026-04-02 17", datetime.datetime(year=2026, month=4, day=2, hour=17, minute=0, second=0)),
        param("2026-04-02", datetime.datetime(year=2026, month=4, day=2, hour=0, minute=0, second=0)),
        param("2026-04", ValueError("Invalid isoformat string: '2026-04'")),
        param("qqq", ValueError("Invalid isoformat string: 'qqq'")),
        param(
            1234567890,
            datetime.datetime(year=2009, month=2, day=13, hour=23, minute=31, second=30, tzinfo=datetime.UTC),
        ),
        param(
            1234567890.123,
            datetime.datetime(
                year=2009, month=2, day=13, hour=23, minute=31, second=30, microsecond=123000, tzinfo=datetime.UTC
            ),
        ),
        param(1234567890123, ValueError("year .*")),
    ],
)
def test_to_datetime(value: Any, expected: datetime.datetime) -> None:
    if isinstance(expected, Exception):
        with pytest.raises(type(expected), match=expected.args[0]):
            to_datetime(value)
    else:
        assert to_datetime(value) == expected
