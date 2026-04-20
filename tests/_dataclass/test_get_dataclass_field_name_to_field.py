import dataclasses
import typing

from type_cast import get_dataclass_field_name_to_field


def test_get_dataclass_field_name_to_field__simple():
    @dataclasses.dataclass
    class ExampleSimpleDataclass:
        integer: int
        string: str

    field_name_to_field = get_dataclass_field_name_to_field(ExampleSimpleDataclass)

    assert set(field_name_to_field.keys()) == {"integer", "string"}
    assert field_name_to_field["integer"].name == "integer"
    assert field_name_to_field["integer"].type == int
    assert field_name_to_field["string"].name == "string"
    assert field_name_to_field["string"].type == str


def test_get_dataclass_field_name_to_field__complex():
    @dataclasses.dataclass
    class ExampleBaseDataclass:
        array: list = dataclasses.field(default_factory=list)

    @dataclasses.dataclass
    class ExampleComplexDataclass(ExampleBaseDataclass):
        integer: dataclasses.InitVar[int] = None
        string: str = "test"

        @property
        def prop(self):
            return 0

        def method(self):
            return self

        @classmethod
        def class_method(cls):
            return 2

        @staticmethod
        def static_method():
            return 3

        def __post_init__(self, integer: int):
            pass

    field_name_to_field = get_dataclass_field_name_to_field(ExampleComplexDataclass)

    assert set(field_name_to_field.keys()) == {"array", "integer", "string"}
    assert field_name_to_field["array"].name == "array"
    assert field_name_to_field["array"].type == list
    assert field_name_to_field["array"].default_factory == list

    assert field_name_to_field["integer"].name == "integer"
    assert field_name_to_field["integer"].type.type == int
    assert isinstance(field_name_to_field["integer"].type, dataclasses.InitVar)
    assert field_name_to_field["integer"].default is None

    assert field_name_to_field["string"].name == "string"
    assert field_name_to_field["string"].type == str
    assert field_name_to_field["string"].default == "test"


def test_get_dataclass_field_name_to_field__init_var():
    @dataclasses.dataclass
    class ExampleComplexDataclass:
        login: dataclasses.InitVar[str] = "default"
        password: dataclasses.InitVar[str] = ""
        auth: typing.Tuple[str, str] = dataclasses.field(init=False)

        def __post_init__(self, login: str, password: str):
            self.auth = (login, password)

    field_name_to_field = get_dataclass_field_name_to_field(ExampleComplexDataclass)

    assert set(field_name_to_field.keys()) == {"login", "password", "auth"}
    assert field_name_to_field["login"].name == "login"
    assert isinstance(field_name_to_field["login"].type, dataclasses.InitVar)
    assert field_name_to_field["login"].default == "default"

    assert field_name_to_field["password"].name == "password"
    assert isinstance(field_name_to_field["password"].type, dataclasses.InitVar)
    assert field_name_to_field["password"].default == ""

    assert field_name_to_field["auth"].name == "auth"
    assert field_name_to_field["auth"].init is False
