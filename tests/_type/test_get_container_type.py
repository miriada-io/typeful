import collections.abc

import pytest

from type_cast import get_container_type


def test_get_container_type():
    with pytest.raises(TypeError):
        get_container_type(collections.abc.Sequence)
    assert get_container_type(collections.abc.Mapping) == dict
    assert get_container_type(collections.abc.Collection) == list
    assert get_container_type(collections.abc.Set) == set

    assert get_container_type(dict) == dict
    assert get_container_type(list) == list
    assert get_container_type(set) == set
    assert get_container_type(frozenset) == frozenset
    assert get_container_type(tuple) == tuple
    assert get_container_type(collections.defaultdict) == collections.defaultdict
    assert get_container_type(collections.deque) == collections.deque

    class MyCustomList(list):
        pass

    class MyOtherList(collections.UserList):
        pass

    assert get_container_type(MyCustomList) == MyCustomList
    assert get_container_type(MyOtherList) == MyOtherList
