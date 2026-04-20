from frozendict import frozendict


class FieldErrors(ValueError):
    def __init__(self, field_to_error: dict[str, Exception]) -> None:
        self.field_to_error = frozendict(field_to_error)


class MissingField(ValueError):
    pass


class UnsupportedType(TypeError):
    pass
