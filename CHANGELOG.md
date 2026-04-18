# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-04-18

### Added
- Initial public release
- Casting utilities: `str_to_bool`, `to_bool`, `to_datetime`, `to_list`, `to_tuple`, `try_cast`, `unflatten_dict`, `url_to_snake_case`
- Type introspection: `is_iterable`, `is_instance`, `is_collection`, `is_mapping`, `is_tuple`, `get_name_from_type`, `get_non_generic_args`, `get_container_type`, `try_extract_type_notes`, `DataclassProtocol`, `eval_forward_refs_in_local_dataclasses`, `get_evaled_dataclass_fields`
- Dataclass conversion: `to_dataclass`, `convert_to_type`, `get_converter`, `get_field_value`, `get_dataclass_field_name_to_field`, `get_dataclass_field_name_to_type`
- Errors: `FieldErrors`, `MissingField`, `UnsupportedType`
- Type aliases: `note`, `AnyType`, `WideType`, `MaybeAnnotated`
- Support for Python 3.11 through 3.14
