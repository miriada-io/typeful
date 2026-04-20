from typing import Any


def unflatten_dict(flatten_dict: dict[str, Any], separator: str = ".") -> dict[str, Any | dict[str, Any]]:
    result: dict[str, Any | dict[str, Any]] = {}
    for key, value in flatten_dict.items():
        container = result
        path = key.split(separator)
        for step in path[:-1]:
            container = container.setdefault(step, {})
        container[path[-1]] = value
    return result
