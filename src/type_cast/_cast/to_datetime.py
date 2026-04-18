import datetime
from typing import Union


def to_datetime(value: Union[str, int, float]) -> datetime.datetime:
    if isinstance(value, str):
        return datetime.datetime.fromisoformat(value)
    return datetime.datetime.fromtimestamp(value, datetime.timezone.utc)
