import dataclasses
import typing

import pytest
import sqlalchemy.orm
from pytest import param

from type_cast import DataclassProtocol, to_dataclass


def test_to_dataclass__simple():
    @dataclasses.dataclass()
    class ExampleSimpleDataclass:
        integer: int
        string: str

    assert to_dataclass(dict(integer=123, string="test"), ExampleSimpleDataclass) == ExampleSimpleDataclass(
        integer=123, string="test"
    )


def test_to_dataclass__union():
    @dataclasses.dataclass()
    class ExampleUnionDataclass:
        integer_or_float: typing.Union[int, float]
        integer_or_float_new: int | float
        optional_string: typing.Optional[str]
        extra_string: typing.Optional[str] = None

    assert to_dataclass(
        dict(integer_or_float="1.23", integer_or_float_new="2.34", optional_string=None), ExampleUnionDataclass
    ) == ExampleUnionDataclass(integer_or_float=1.23, integer_or_float_new=2.34, optional_string=None)


def test_to_dataclass__complex():
    @dataclasses.dataclass()
    class ExampleComplexDataclass:
        limit: dataclasses.InitVar[int]
        offset: int = 0
        last: int = dataclasses.field(init=False)
        array: list = dataclasses.field(default_factory=list)

        def __post_init__(self, limit: int):
            self.last = self.offset + limit

    assert to_dataclass(dict(limit=123), ExampleComplexDataclass) == ExampleComplexDataclass(limit=123)


def test_to_dataclass__nested():
    @dataclasses.dataclass()
    class ExampleDelegateDataclass:
        integer: int

    @dataclasses.dataclass()
    class ExampleNestedDataclass:
        first: ExampleDelegateDataclass
        second: ExampleDelegateDataclass

    assert to_dataclass(
        {"first": {"integer": 123}, "second": {"integer": 678}}, ExampleNestedDataclass
    ) == ExampleNestedDataclass(
        first=ExampleDelegateDataclass(integer=123), second=ExampleDelegateDataclass(integer=678)
    )


def test_to_dataclass__complex_nested():
    @dataclasses.dataclass(unsafe_hash=True, frozen=True)
    class ExampleKeyDataclass:
        integer: int

    @dataclasses.dataclass()
    class ExampleValueDataclass:
        string: str

    @dataclasses.dataclass()
    class ExampleNestedDataclass:
        dict_: typing.Dict[int, ExampleValueDataclass]
        list_: typing.List[ExampleValueDataclass]
        dict_of_sets: typing.Dict[int, typing.Set[ExampleKeyDataclass]]

    assert to_dataclass(
        {
            "dict_": {123: {"string": "test"}, 234: {"string": "passed"}},
            "list_": [{"string": "12"}, {"string": "23"}],
            "dict_of_sets": {0: [], 1: [{"integer": 11}], 2: [{"integer": 22}, {"integer": 22}, {"integer": 3}]},
        },
        ExampleNestedDataclass,
    ) == ExampleNestedDataclass(
        dict_={123: ExampleValueDataclass("test"), 234: ExampleValueDataclass("passed")},
        list_=[ExampleValueDataclass("12"), ExampleValueDataclass("23")],
        dict_of_sets={0: set(), 1: {ExampleKeyDataclass(11)}, 2: {ExampleKeyDataclass(22), ExampleKeyDataclass(3)}},
    )


def test_to_dataclass__annotated():
    @dataclasses.dataclass()
    class ExampleDelegateDataclass:
        integer: typing.Annotated[int, "Integer"]

    @dataclasses.dataclass()
    class ExampleNestedDataclass:
        first: typing.Annotated[ExampleDelegateDataclass, "First"]
        second: typing.Annotated[ExampleDelegateDataclass, "Second"]

    assert to_dataclass(
        {"first": {"integer": 123}, "second": {"integer": 678}}, typing.Annotated[ExampleNestedDataclass, "Target type"]
    ) == ExampleNestedDataclass(
        first=ExampleDelegateDataclass(integer=123), second=ExampleDelegateDataclass(integer=678)
    )


@dataclasses.dataclass
class RecursiveDC:
    children: list["RecursiveDC"]


@pytest.mark.parametrize(
    ["payload", "expected"],
    [
        param({"children": []}, RecursiveDC([])),
        param(
            {"children": [{"children": [{"children": []}]}, {"children": []}]},
            RecursiveDC([RecursiveDC([RecursiveDC([])]), RecursiveDC([])]),
        ),
        param(
            {"children": [{"children": [{"children": []}]}, {"children": []}]},
            RecursiveDC([RecursiveDC([RecursiveDC([])]), RecursiveDC([])]),
        ),
    ],
)
def test_recursive_to_dataclass(payload: dict, expected: RecursiveDC):
    assert to_dataclass(payload, RecursiveDC) == expected


sqlalchemy_mapper_registry = sqlalchemy.orm.registry()


@sqlalchemy_mapper_registry.mapped_as_dataclass
class Parent:
    __tablename__ = "parent_table"
    id: sqlalchemy.orm.Mapped[int | None] = sqlalchemy.orm.mapped_column(primary_key=True, init=False)
    children: sqlalchemy.orm.Mapped[list["Child"]] = sqlalchemy.orm.relationship(
        back_populates="parent", default_factory=list
    )


@sqlalchemy_mapper_registry.mapped_as_dataclass
class Child:
    __tablename__ = "child_table"
    id: sqlalchemy.orm.Mapped[int | None] = sqlalchemy.orm.mapped_column(primary_key=True, init=False)
    parent_id: sqlalchemy.orm.Mapped[int | None] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("parent_table.id"), default=None
    )
    parent: sqlalchemy.orm.Mapped["Parent | None"] = sqlalchemy.orm.relationship(
        back_populates="children", default=None, compare=False, repr=False
    )


@pytest.mark.parametrize(
    ["payload", "target_type", "expected"],
    [
        param({"children": []}, Parent, Parent(children=[])),
        param({"children": [{}]}, Parent, Parent(children=[Child()])),
        param({"children": [{"parent_id": 1}, {}]}, Parent, Parent(children=[Child(parent_id=1), Child()])),
    ],
)
def test_mapped_recursive_to_dataclass(payload: dict, target_type: type[DataclassProtocol], expected: RecursiveDC):
    assert to_dataclass(payload, target_type) == expected
