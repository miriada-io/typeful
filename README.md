# typeful

[![PyPI](https://img.shields.io/pypi/v/typeful.svg?label=PyPI)](https://pypi.org/project/typeful/)
[![Python](https://img.shields.io/pypi/pyversions/typeful.svg?label=Python)](https://pypi.org/project/typeful/)
[![Tests](https://github.com/miriada-io/typeful/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/miriada-io/typeful/actions/workflows/tests.yml)
[![License](https://img.shields.io/pypi/l/typeful.svg?label=License)](https://github.com/miriada-io/typeful/blob/master/LICENSE)

Tools to introspect, validate, and cast Python types at runtime.

## Installation

```bash
pip install typeful
```

Requires Python 3.11+.

## Why typeful?

Python's built-in introspection and construction tools break in ordinary real-world cases:

- `isinstance(x, dict[str, int])` raises `TypeError` — no generics support. `is_instance` handles generics, unions, and nested containers.
- `bool("false")` returns `True` — any non-empty string is truthy. `to_bool` understands `"true"/"false"/"yes"/"no"/"on"/"off"/"1"/"0"`.
- `list("abc")` returns `['a','b','c']` and `list(None)` raises. `to_list` / `to_tuple` give you the intuitive behavior.
- `datetime.fromisoformat` doesn't accept timestamps; `datetime.fromtimestamp` doesn't accept strings. `to_datetime` accepts both.
- `str(typing.List[int])` prints `'typing.List[int]'` — ugly in logs and errors. `get_name_from_type` returns `'list[int]'`.
- Turning `{"name": "Alice", "age": "30", "address": {...}}` into a nested dataclass with automatic type coercion is a one-liner with `to_dataclass` — no schemas, no models, no declaration beyond the dataclass itself.

No pydantic-style model hierarchies. No metaclass magic. Plain dataclasses and plain values.

## Quick Start

```python
from dataclasses import dataclass, field
from typeful import to_dataclass, FieldErrors

@dataclass
class Address:
    city: str
    zip_code: int

@dataclass
class User:
    name: str
    age: int
    address: Address
    tags: list[str] = field(default_factory=list)

# Realistic payload — mixed strings and nested structures (e.g. from a form, config, or JSON):
payload = {
    "name": "Alice",
    "age": "30",                                            # str → int
    "address": {"city": "Springfield", "zip_code": "12345"},  # nested dict → nested dataclass
    "tags": ["admin", "editor"],
}

user = to_dataclass(payload, User)
# User(name='Alice', age=30, address=Address(city='Springfield', zip_code=12345), tags=['admin', 'editor'])

# Invalid inputs aggregate into a single error, keyed by dotted field path:
try:
    to_dataclass({"name": "Bob", "age": "abc", "address": {"city": "X", "zip_code": "Y"}}, User)
except FieldErrors as e:
    print(dict(e.field_to_error))
    # {'age': ValueError(...), 'address.zip_code': ValueError(...)}
```

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
from typeful import str_to_bool

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

*Use when:* the built-in `bool()` is unsafe for strings — `bool("false")` returns `True`.

```python
from typeful import to_bool

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

*Use when:* you don't know upfront whether the value is an ISO string or a Unix timestamp — `datetime.fromisoformat` rejects timestamps; `datetime.fromtimestamp` rejects strings.

```python
from typeful import to_datetime

to_datetime("2026-04-02T17:10:01")        # datetime(2026, 4, 2, 17, 10, 1)
to_datetime("2026-04-02 17:10:01+03:00")  # datetime(2026, 4, 2, 17, 10, 1, tzinfo=timezone(timedelta(seconds=10800)))
to_datetime("2026-04-02")                 # datetime(2026, 4, 2, 0, 0)
to_datetime(1234567890)                   # datetime(2009, 2, 13, 23, 31, 30, tzinfo=timezone.utc)
to_datetime(1234567890.123)               # datetime(2009, 2, 13, 23, 31, 30, 123000, tzinfo=timezone.utc)
```

### `to_list`

Converts an iterable to a list, wraps non-iterables, handles `None`.

*Use when:* built-in `list()` does the wrong thing: `list("abc")` unpacks into `['a','b','c']` and `list(None)` raises.

```python
from typeful import to_list

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
from typeful import to_tuple

to_tuple([1, 2, 3])            # (1, 2, 3)
to_tuple(1)                    # (1,)
to_tuple(None)                 # ()
to_tuple("foo")                # ("foo",)
to_tuple("foo", base_type=None)  # ("f", "o", "o")
```

### `try_cast`

Attempts to cast a value; returns a fallback on failure.

```python
from typeful import try_cast

try_cast("123", int)                    # 123
try_cast("abc", int)                    # None (default fallback)
try_cast("abc", int, "default")         # "default"
try_cast("abc", int, ..., TypeError)    # raises ValueError (not caught by TypeError)
```

### `unflatten_dict`

Converts a flat dictionary with dot-separated keys into a nested one.

```python
from typeful import unflatten_dict

unflatten_dict({"db.host": "localhost", "db.port": 5432})
# {"db": {"host": "localhost", "port": 5432}}

unflatten_dict({"a/b/c": 1}, separator="/")
# {"a": {"b": {"c": 1}}}
```

### `url_to_snake_case`

Converts a URL to a snake_case string.

```python
from typeful import url_to_snake_case

url_to_snake_case("http://google.com")
# "http_google_com"

url_to_snake_case("https://example.com/api/v1")
# "https_example_com_api_v1"
```

---

## Type Introspection

### `is_iterable`

Checks if an object is iterable. Strings, bytes, dicts, and generic aliases are excluded by default.

*Use when:* `hasattr(x, '__iter__')` is too loose — it treats strings and dicts as iterables, which is almost never what you want when processing a "collection of items".

```python
from typeful import is_iterable

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

*Use when:* built-in `isinstance(x, list[int])` raises `TypeError`. This library's version validates element types recursively.

```python
from typeful import is_instance

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
from typeful import is_collection

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
from typeful import is_mapping

is_mapping({}, [int, int])                    # True (empty)
is_mapping({1: 2, 3: 4}, [int, int])         # True
is_mapping({"a": 1}, [str, int])             # True
is_mapping({"a": 1}, [int, int])             # False (keys are str)
is_mapping({1: "a", "b": 2}, [int | str, int | str])  # True
```

### `is_tuple`

Checks if a value is a tuple matching a type signature. Supports fixed-length and variable-length (with `...`).

```python
from typeful import is_tuple

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

*Use when:* writing log messages or error strings. `str(typing.List[int])` renders as `'typing.List[int]'`; `repr(str | None)` is an awkward `'str | None'` only for the pipe-syntax form. This gives you one consistent compact form for everything.

```python
from typeful import get_name_from_type

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

*Use when:* you need to enumerate every leaf type that can appear inside a composite annotation — e.g. to register converters, to build a union of acceptable types, or to walk the type shape of a field.

```python
from typeful import get_non_generic_args

get_non_generic_args(dict[int, str | None])
# (int, str, NoneType)

get_non_generic_args(dict[int | str, list[bool | None] | set[float]])
# (int, str, bool, NoneType, float)
```

### `get_container_type`

Maps abstract container types to their concrete implementations.

*Use when:* you receive annotations like `Mapping[str, int]` or `Collection[int]` and need a real class to construct. `collections.abc` types can't be instantiated directly — this picks a sensible concrete type (`dict`, `list`, `set`).

```python
import collections.abc
from typeful import get_container_type

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

*Use when:* a function accepts both plain types (`int`) and `Annotated[int, ...]` and you need to work with both uniformly — the base type on one side, the metadata on the other.

```python
from typing import Annotated
from typeful import try_extract_type_notes

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
from typeful import DataclassProtocol

@dataclass
class User:
    name: str

isinstance(User, DataclassProtocol)    # True
isinstance(User(), DataclassProtocol)  # True
isinstance("string", DataclassProtocol)  # False
```

### `eval_forward_refs_in_local_dataclasses`

Context manager that resolves forward references in locally-defined dataclasses.

*Use when:* you declare a dataclass inside a function or other local scope and it references itself (`list["Self"]`). Python's default machinery can't find `"Self"` in the local namespace, so the reference stays as an unresolved string. The context manager captures the calling frame and resolves it.

```python
from dataclasses import dataclass
from typeful import eval_forward_refs_in_local_dataclasses, get_evaled_dataclass_fields

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

*Use when:* you have a dict (from JSON, config file, ORM row, or form input) and you want it typed as a dataclass, with strings coerced to ints, nested dicts turned into nested dataclasses, and errors aggregated per field — without declaring a Pydantic model, a schema, or a converter.

```python
from dataclasses import dataclass
from typeful import to_dataclass

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

to_dataclass({"name": "Alice", "address": {"city": "Springfield"}}, User)
# User(name="Alice", address=Address(city="Springfield"))
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
user = User(name="Alice", address=Address(city="Springfield"))
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

*Use when:* you have one value and one target type — no dataclass involved. It's the one-liner for "cast this string to `list[int]`" and similar. Internally calls `get_converter` and applies the result.

```python
from typeful import convert_to_type

convert_to_type(int, "42")               # 42
convert_to_type(bool, "yes")             # True
convert_to_type(list[int], [1, 2, 3])    # [1, 2, 3]
convert_to_type(list[int], ["1", "2"])   # [1, 2] — each element cast to int
```

**String values for container types are parsed as JSON** (via `json.loads`), then each element is cast to the inner type:

```python
convert_to_type(list[int], "[1, 2]")            # [1, 2]
convert_to_type(dict[str, int], '{"a": 1}')     # {"a": 1}
convert_to_type(tuple[int, ...], "[1, 2, 3]")   # (1, 2, 3)

convert_to_type(list[int], "['a']")  # raises json.JSONDecodeError — single quotes aren't JSON
convert_to_type(list[int], 123)      # raises ValueError — not iterable
```

### `get_converter`

Returns a cached converter function for a given type. Used internally by `to_dataclass` and `convert_to_type`.

*Use when:* you want the converter **function** as a first-class value — to store in a registry, pass as a callback, or apply repeatedly to many values. For a one-shot conversion, prefer [`convert_to_type`](#convert_to_type).

```python
from typeful import get_converter

int_converter = get_converter(int)
int_converter("42")  # 42

bool_converter = get_converter(bool)
bool_converter("yes")  # True

list_int_converter = get_converter(list[int])
list_int_converter([1, 2, 3])     # [1, 2, 3] — passes through
list_int_converter("[1, 2, 3]")   # [1, 2, 3] — parses JSON string

dict_converter = get_converter(dict[str, int])
dict_converter('{"a": 1}')        # {"a": 1} — parses JSON string

tuple_converter = get_converter(tuple[int, ...])
tuple_converter("[1, 2, 3]")      # (1, 2, 3) — parses JSON string
```

For `list`, `tuple`, `set`, `frozenset`, `dict`: string values are parsed as JSON before element casting. Python literal syntax (single quotes) is **not** accepted — use valid JSON.

Supported types: `str`, `int`, `float`, `bool`, `datetime.datetime`, `datetime.date`, `datetime.time`, `typing.Any`, dataclasses, unions, `list`, `tuple`, `set`, `frozenset`, `dict`, `InitVar`.

### `get_dataclass_field_name_to_field`

Returns a frozen dict mapping field names to `dataclasses.Field` objects.

```python
from dataclasses import dataclass, field, InitVar
from typeful import get_dataclass_field_name_to_field

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
from typeful import to_dataclass, FieldErrors

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
from typeful import to_dataclass, FieldErrors, MissingField

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
from typeful import note, AnyType, WideType, MaybeAnnotated

# note — alias for typing.Annotated
x: note[int, "positive"] = 42

# AnyType — matches any type, union, generic alias, or Annotated type
isinstance(list[int], AnyType)                    # True
isinstance(int | str, AnyType)                    # True
isinstance(typing.Annotated[int, "x"], AnyType)   # True
isinstance(42, AnyType)                           # False (value, not type)
```

---

## Deprecated Aliases

The following names are kept for backward compatibility. They are thin wrappers that emit a `DeprecationWarning` — prefer the canonical names in new code.

| Deprecated | Use instead |
| --- | --- |
| `dict_to_dataclass(data, cls)` | [`to_dataclass(data, cls)`](#to_dataclass) |
| `convert(type_, init, default, default_factory, value)` | `get_field_value(type_, init, default, default_factory, value)` |

Both aliases forward all arguments unchanged; behavior is identical. They will be removed in a future major release.

## License

[MIT](LICENSE)
