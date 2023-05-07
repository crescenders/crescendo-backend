from typing import Protocol, TypeVar


class Identifiable(Protocol):
    id: int


BaseEntity = TypeVar("BaseEntity", bound=Identifiable)
