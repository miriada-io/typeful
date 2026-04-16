# type-cast

[![Tests](https://github.com/miriada-io/type-cast/actions/workflows/tests.yml/badge.svg)](https://github.com/miriada-io/type-cast/actions/workflows/tests.yml)
[![License](https://img.shields.io/github/license/miriada-io/type-cast)](LICENSE)

Tools to introspect, validate, and cast Python types at runtime.

## Installation

```bash
pip install type-cast
```

Requires Python 3.11+.

## Overview

**Casting:** [`str_to_bool`](#str_to_bool) | [`to_bool`](#to_bool) | [`to_datetime`](#to_datetime) | [`to_list`](#to_list) | [`to_tuple`](#to_tuple) | [`try_cast`](#try_cast) | [`unflatten_dict`](#unflatten_dict) | [`url_to_snake_case`](#url_to_snake_case)

**Type Introspection:** [`is_iterable`](#is_iterable) | [`is_instance`](#is_instance) | [`is_collection`](#is_collection) | [`is_mapping`](#is_mapping) | [`is_tuple`](#is_tuple) | [`get_name_from_type`](#get_name_from_type) | [`get_non_generic_args`](#get_non_generic_args) | [`get_container_type`](#get_container_type) | [`try_extract_type_notes`](#try_extract_type_notes) | [`DataclassProtocol`](#dataclassprotocol) | [`eval_forward_refs_in_local_dataclasses`](#eval_forward_refs_in_local_dataclasses)

**Dataclass Conversion:** [`to_dataclass`](#to_dataclass) | [`convert_to_type`](#convert_to_type) | [`get_converter`](#get_converter) | [`get_dataclass_field_name_to_field`](#get_dataclass_field_name_to_field)

**Errors:** [`FieldErrors`](#fielderrors) | [`MissingField`](#missingfield) | [`UnsupportedType`](#unsupportedtype)

**Type Aliases:** [`note`](#type-aliases) | [`AnyType`](#type-aliases) | [`WideType`](#type-aliases) | [`MaybeAnnotated`](#type-aliases)

---

## Casting

### `str_to_bool`

Converts a string to `bool`. Case-insensitive.

```python
from type_cast import str_to_bool

str_to_bool("true")   # True
str_to_bool("1")      # True
str_to_bool("on")     # True
str_to_bool("+")      # True
str_to_bool("yes")    # True

str_to_bool("false")  # False
str_to_bool("0")      # False
str_to_bool("off")    # False
str_to_bool("-")      # False
str_to_bool("no")     # False

str_to_bool("maybe")  # raises ValueError
```

### `to_bool`

Converts `bool`, `int`, or `str` to `bool`.

```python
from type_cast import to_bool

to_bool(True)    # True
to_bool(1)       # True
to_bool(-1)      # True
to_bool(0)       # False
to_bool("yes")   # True
to_bool("off")   # False

to_bool([])      # raises TypeError
```

### `to_datetime`

Converts an ISO format string or a numeric timestamp to `datetime`.

```python
from type_cast import to_datetime

to_datetime("2026-04-02T17:10:01")        # datetime(2026, 4, 2, 17, 10, 1)
to_datetime("2026-04-02 17:10:01+03:00")  # datetime(2026, 4, 2, 17, 10, 1, tzinfo=timezone(timedelta(seconds=10800)))
to_datetime("2026-04-02")                 # datetime(2026, 4, 2, 0, 0)
to_datetime(1234567890)                   # datetime(2009, 2, 13, 23, 31, 30, tzinfo=timezone.utc)
to_datetime(1234567890.123)               # datetime(2009, 2, 13, 23, 31, 30, 123000, tzinfo=timezone.utc)
```

### `to_list`

Converts an iterable to a list, wraps non-iterables, handles `None`.

```python
from type_cast import to_list

to_list((1, 2, 3))             # [1, 2, 3]
to_list(1)                     # [1]
to_list(None)                  # []
to_list(None, none=None)       # None
to_list(None, none=lambda: [0])  # [0]

# Strings and dicts are NOT unpacked by default:
to_list("foo")                 # ["foo"]
to_list({"a": 1})              # [{"a": 1}]

# Override with base_type:
to_list("foo", base_type=None)           # ["f", "o", "o"]
to_list((1, 2), base_type=(tuple,))      # [(1, 2)]
```

### `to_tuple`

Same as `to_list`, but returns a `tuple`.

```python
from type_cast import to_tuple

to_tuple([1, 2, 3])            # (1, 2, 3)
to_tuple(1)                    # (1,)
to_tuple(None)                 # ()
to_tuple("foo")                # ("foo",)
to_tuple("foo", base_type=None)  # ("f", "o", "o")
```

### `try_cast`

Attempts to cast a value; returns a fallback on failure.

```python
from type_cast import try_cast

try_cast("123", int)                    # 123
try_cast("abc", int)                    # None (default fallback)
try_cast("abc", int, "default")         # "default"
try_cast("abc", int, ..., TypeError)    # raises ValueError (not caught by TypeError)
```

### `unflatten_dict`

Converts a flat dictionary with dot-separated keys into a nested one.

```python
from type_cast import unflatten_dict

unflatten_dict({"db.host": "localhost", "db.port": 5432})
# {"db": {"host": "localhost", "port": 5432}}

unflatten_dict({"a/b/c": 1}, separator="/")
# {"a": {"b": {"c": 1}}}
```

### `url_to_snake_case`

Converts a URL to a snake_case string.

```python
from type_cast import url_to_snake_case

url_to_snake_case("http://ya.ru")
# "http_ya_ru"

url_to_snake_case("https://example.com/api/v1")
# "https_example_com_api_v1"
```

---

## Type Introspection

### `is_iterable`

Checks if an object is iterable. Strings, bytes, dicts, and generic aliases are excluded by default.

```python
from type_cast import is_iterable

is_iterable([1, 2, 3])    # True
is_iterable((1,))         # True
is_iterable(set())        # True
is_iterable({}.values())  # True

is_iterable("foo")        # False (string excluded)
is_iterable({})           # False (dict excluded)
is_iterable(1)            # False
is_iterable(None)         # None

# Override exclusions:
is_iterable("foo", base_type=None)       # True
is_iterable([1, 2], base_type=(list,))   # False (list now excluded)
```

### `is_instance`

Advanced `isinstance` that supports generic types, unions, and nested containers.

```python
from type_cast import is_instance

# Basic types
is_instance(1, int)               # True
is_instance(1, str)               # False

# Union types
is_instance(1, int | str)         # True
is_instance(1, [int, str])        # True (list = any of)

# Generic containers
is_instance({"a": 1}, dict[str, int])           # True
is_instance({"a": 1, "b": 2.0}, dict[str, int]) # False (2.0 is float)
is_instance([1.1, 2.2], list[float])             # True

# Tuples (fixed-length)
is_instance((1, "x"), tuple[int, str])  # True
is_instance((1,), tuple[int, str])      # False (wrong length)

# Nested generics
is_instance({"a": 1, "b": "x"}, dict[str, int | str])  # True

# typing.Any matches everything
is_instance("anything", typing.Any)  # True
```

### `is_collection`

Checks if a value is a collection with elements of a given type.

```python
from type_cast import is_collection

is_collection([1, 2, 3], [int])         # True
is_collection([1, "2", 3], [int])       # False
is_collection([1, "2"], [int | str])    # True
is_collection([], [int])                # True (empty is valid)
is_collection(set(), [])                # True (no type constraint)
is_collection("not a collection", [])   # False
```

### `is_mapping`

Checks if a value is a mapping with keys/values of given types.

```python
from type_cast import is_mapping

is_mapping({}, [int, int])                    # True (empty)
is_mapping({1: 2, 3: 4}, [int, int])         # True
is_mapping({"a": 1}, [str, int])             # True
is_mapping({"a": 1}, [int, int])             # False (keys are str)
is_mapping({1: "a", "b": 2}, [int | str, int | str])  # True
```

### `is_tuple`

Checks if a value is a tuple matching a type signature. Supports fixed-length and variable-length (with `...`).

```python
from type_cast import is_tuple

# Fixed-length
is_tuple((1, "x"), [int, str])          # True
is_tuple((1,), [int, str])              # False (wrong length)
is_tuple((1,), [int])                   # True

# Variable-length with ellipsis
is_tuple((1, 2, 3), [int, ...])         # True
is_tuple(("a", "b"), [str, ...])        # True
is_tuple(("a", 1), [str, ...])          # False (1 is not str)

# Repeating pattern
is_tuple(("a", 1, "b", 2), [str, int, ...])  # True
is_tuple(("a", 1, "b"), [str, int, ...])      # True

# No constraint
is_tuple((1, "a", 3.14), [])            # True (any tuple)
```

### `get_name_from_type`

Returns a compact, readable name for a type.

```python
from type_cast import get_name_from_type

get_name_from_type(str)                   # "str"
get_name_from_type(None)                  # "None"
get_name_from_type(list[int])             # "list[int]"
get_name_from_type(dict[str, int])        # "dict[str, int]"
get_name_from_type(tuple[int, ...])       # "tuple[int, ...]"
get_name_from_type(str | int)             # "str | int"
get_name_from_type(str | None)            # "str | None"
get_name_from_type(typing.Optional[str])  # "str | None"
```

### `get_non_generic_args`

Flattens nested generic type arguments into a flat tuple of concrete types.

```python
from type_cast import get_non_generic_args

get_non_generic_args(dict[int, str | None])
# (int, str, NoneType)

get_non_generic_args(dict[int | str, list[bool | None] | set[float]])
# (int, str, bool, NoneType, float)
```

### `get_container_type`

Maps abstract container types to their concrete implementations.

```python
import collections.abc
from type_cast import get_container_type

get_container_type(collections.abc.Mapping)     # dict
get_container_type(collections.abc.Collection)  # list
get_container_type(collections.abc.Set)         # set

# Concrete types pass through unchanged:
get_container_type(dict)       # dict
get_container_type(frozenset)  # frozenset
get_container_type(tuple)      # tuple
```

### `try_extract_type_notes`

Extracts the base type and annotation metadata from `Annotated` types.

```python
from typing import Annotated
from type_cast import try_extract_type_notes

try_extract_type_notes(int)
# (int, ())

try_extract_type_notes(Annotated[int, "positive"])
# (int, ("positive",))

try_extract_type_notes(Annotated[int, "positive", "nonzero"])
# (int, ("positive", "nonzero"))
```

### `DataclassProtocol`

A runtime-checkable protocol that matches any dataclass type or instance.

```python
from dataclasses import dataclass
from type_cast import DataclassProtocol

@dataclass
class User:
    name: str

isinstance(User, DataclassProtocol)    # True
isinstance(User(), DataclassProtocol)  # True
isinstance("string", DataclassProtocol)  # False
```

### `eval_forward_refs_in_local_dataclasses`

Context manager that resolves forward references in locally-defined dataclasses.

```python
from dataclasses import dataclass
from type_cast import eval_forward_refs_in_local_dataclasses, get_evaled_dataclass_fields

with eval_forward_refs_in_local_dataclasses():
    @dataclass
    class Node:
        id: int
        children: list["Node"]

get_evaled_dataclass_fields(Node)
# frozendict({"id": int, "children": list[Node]})
```

Without the context manager, `list["Node"]` would remain an unresolved string reference.

---

## Dataclass Conversion

### `to_dataclass`

Converts a dict (or any object) to a dataclass instance with automatic type casting.

```python
from dataclasses import dataclass
from type_cast import to_dataclass

@dataclass
class User:
    name: str
    age: int

# Basic conversion with type casting:
to_dataclass({"name": "Alice", "age": "30"}, User)
# User(name="Alice", age=30) — "30" is cast to int
```

**Nested dataclasses:**

```python
@dataclass
class Address:
    city: str

@dataclass
class User:
    name: str
    address: Address

to_dataclass({"name": "Alice", "address": {"city": "Moscow"}}, User)
# User(name="Alice", address=Address(city="Moscow"))
```

**Union types:**

```python
@dataclass
class Config:
    value: int | float
    label: str | None = None

to_dataclass({"value": "1.5"}, Config)
# Config(value=1.5, label=None)
```

**Collections:**

```python
@dataclass
class Team:
    members: list[str]
    scores: dict[str, int]

to_dataclass({"members": ["a", "b"], "scores": {"a": 1, "b": 2}}, Team)
# Team(members=["a", "b"], scores={"a": 1, "b": 2})
```

**Annotated types:**

```python
from typing import Annotated

@dataclass
class Item:
    value: Annotated[int, "positive"]

to_dataclass({"value": "42"}, Annotated[Item, "validated"])
# Item(value=42) — annotations are stripped, type casting still works
```

**Passthrough — if value is already the target type:**

```python
user = User(name="Alice", address=Address(city="Moscow"))
to_dataclass(user, User) is user  # True — returned as-is
```

**From an arbitrary object (via getattr):**

```python
class Row:
    name = "Alice"
    age = 30

to_dataclass(Row(), User)  # User(name="Alice", age=30)
```

### `convert_to_type`

Converts a single value to a target type using the registered converter.

```python
from type_cast import convert_to_type

convert_to_type(int, "42")          # 42
convert_to_type(bool, "yes")        # True
convert_to_type(list[int], "[1,2]") # [1, 2]
```

### `get_converter`

Returns a cached converter function for a given type. Used internally by `to_dataclass` and `convert_to_type`.

```python
from type_cast import get_converter

int_converter = get_converter(int)
int_converter("42")  # 42

bool_converter = get_converter(bool)
bool_converter("yes")  # True

list_int_converter = get_converter(list[int])
list_int_converter("[1, 2, 3]")  # [1, 2, 3] (parses JSON string)
list_int_converter([1, 2, 3])    # [1, 2, 3] (passes through)
```

Supported types: `str`, `int`, `float`, `bool`, `datetime.datetime`, `datetime.date`, `datetime.time`, `typing.Any`, dataclasses, unions, `list`, `tuple`, `set`, `frozenset`, `dict`, `InitVar`.

### `get_dataclass_field_name_to_field`

Returns a frozen dict mapping field names to `dataclasses.Field` objects.

```python
from dataclasses import dataclass, field, InitVar
from type_cast import get_dataclass_field_name_to_field

@dataclass
class Config:
    host: str
    port: int = 8080
    tags: list = field(default_factory=list)

fields = get_dataclass_field_name_to_field(Config)
fields["host"].name          # "host"
fields["port"].default       # 8080
fields["tags"].default_factory  # list
```

---

## Error Handling

### `FieldErrors`

Raised by `to_dataclass` when one or more fields fail to convert. Contains a `field_to_error` dict.

```python
from dataclasses import dataclass
from type_cast import to_dataclass, FieldErrors

@dataclass
class Strict:
    x: int
    y: int

try:
    to_dataclass({"x": "abc", "y": "def"}, Strict)
except FieldErrors as e:
    print(e.field_to_error)
    # frozendict({"x": ValueError(...), "y": ValueError(...)})
```

### `MissingField`

Raised when a required field has no value, no default, and no default_factory.

```python
from type_cast import to_dataclass, FieldErrors, MissingField

@dataclass
class Required:
    name: str

try:
    to_dataclass({}, Required)
except FieldErrors as e:
    isinstance(e.field_to_error["name"], MissingField)  # True
```

### `UnsupportedType`

Raised by `convert_to_type` when the target type has no registered converter.

---

## Type Aliases

The library exports several type aliases useful for type introspection:

```python
from type_cast import note, AnyType, WideType, MaybeAnnotated

# note — alias for typing.Annotated
x: note[int, "positive"] = 42

# AnyType — matches any type, union, generic alias, or Annotated type
isinstance(list[int], AnyType)                    # True
isinstance(int | str, AnyType)                    # True
isinstance(typing.Annotated[int, "x"], AnyType)   # True
isinstance(42, AnyType)                           # False (value, not type)
```

## License

[MIT](LICENSE)
