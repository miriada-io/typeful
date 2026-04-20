import dataclasses

from type_cast import eval_forward_refs_in_local_dataclasses, get_evaled_dataclass_fields


def test_eval_forward_refs_in_local_dataclasses():
    with eval_forward_refs_in_local_dataclasses():

        @dataclasses.dataclass
        class Node:
            id: int | None
            children: list["Node"]

    assert get_evaled_dataclass_fields(Node) == {"children": list[Node], "id": int | None}
