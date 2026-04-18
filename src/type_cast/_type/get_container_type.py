import collections.abc


def get_container_type(type_origin) -> type:
    if not getattr(type_origin, "__abstractmethods__", None):
        return type_origin
    container_type = ORIGIN_TO_CONTAINER_TYPE.get(type_origin)
    if container_type is None:
        raise TypeError(f'Attempt to get_container_type from unexpected origin: {type_origin}')

    return container_type


ORIGIN_TO_CONTAINER_TYPE: dict[collections.abc.Container, type] = {
    collections.abc.Mapping: dict,
    collections.abc.Collection: list,
    collections.abc.Set: set,
}
