import datetime


def to_datetime(value: str | int | float) -> datetime.datetime:
    if isinstance(value, str):
        return datetime.datetime.fromisoformat(value)
    return datetime.datetime.fromtimestamp(value, datetime.UTC)
