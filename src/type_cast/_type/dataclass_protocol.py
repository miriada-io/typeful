from typing import Any, ClassVar, Protocol, runtime_checkable


# Matches any class with a `__dataclass_fields__` attribute (i.e. any dataclass).
# An alternative form using `@dataclasses.dataclass` decorator on the Protocol is
# recognized by PyCharm but rejected by mypy and breaks in Python 3.14+.
@runtime_checkable
class DataclassProtocol(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]]
