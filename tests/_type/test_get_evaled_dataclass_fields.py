import dataclasses

import pytest

from typeful import eval_forward_refs_in_local_dataclasses, get_evaled_dataclass_fields


def test_get_evaled_dataclass_fields__local_dc():
    @dataclasses.dataclass
    class Node:
        id: int | None
        children: list["Node"]

    with pytest.raises(TypeError):
        get_evaled_dataclass_fields(Node)


def test_get_evaled_dataclass_fields__evaled_sqlalchemy_local_dc():
    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

    sqlalchemy_mapper_registry = registry()
    with eval_forward_refs_in_local_dataclasses():

        @sqlalchemy_mapper_registry.mapped_as_dataclass
        class Parent:
            __tablename__ = "parent_table"
            id: Mapped[int | None] = mapped_column(primary_key=True, init=False)
            children: Mapped[list["Child"]] = relationship(back_populates="parent")

        @sqlalchemy_mapper_registry.mapped_as_dataclass
        class Child:
            __tablename__ = "child_table"
            id: Mapped[int | None] = mapped_column(primary_key=True, init=False)
            parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"), default=None)
            parent: Mapped["Parent | None"] = relationship(back_populates="children", default=None)

    assert get_evaled_dataclass_fields(Parent) == {"id": int | None, "children": list[Child]}
    assert get_evaled_dataclass_fields(Child) == {"id": int | None, "parent_id": int, "parent": Parent | None}
