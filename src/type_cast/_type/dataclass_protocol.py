import dataclasses
from typing import runtime_checkable, Protocol, ClassVar, Any


# PyCharm compatible, but incompatible with MyPy AND DOES NOT WORK in 3.14+
@runtime_checkable
@dataclasses.dataclass
class DataclassProtocol(Protocol):
    pass


# MyPy compatible, but incompatible with PyCharm
@runtime_checkable
class DataclassProtocol(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]]
