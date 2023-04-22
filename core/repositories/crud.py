from abc import ABC, abstractmethod
from typing import Generic, List, Optional

from core.repositories.base import BaseRepository
from core.repositories.type import T


class CRUDRepositoryABC(BaseRepository, ABC, Generic[T]):
    """The Base CRUD Repository class."""

    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Save the given entity.

        :param entity: Entity to save.
        :return: saved Entity
        """
        pass

    @abstractmethod
    def save_all(self, entities: List[T]) -> List[T]:
        """
        Save all given entities.

        :param entities: Entities to save.
        :return: saved Entities.
        """
        pass

    @abstractmethod
    def read_by_eid(self, eid) -> Optional[T]:
        """
        Read the entity with given eid.

        :return: if entity is found with given eid, return it, else return None
        """
        pass

    @abstractmethod
    def is_exists_by_eid(self) -> bool:
        """
        Check if entity with given eid exists.

        :return: if entity is found with given eid, return True, else return False
        """
        pass

    @abstractmethod
    def read_all(self) -> List[T]:
        """
        Read all entities.

        :return: list of all entities.
        """
        pass

    @abstractmethod
    def read_all_by_eids(self, ids: List[int]) -> List[T]:
        """
        Read all entities with given eids.

        :return: list of all entities, with given eids.
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """Count all entities."""
        pass

    @abstractmethod
    def delete_by_eid(self, eid: int) -> None:
        """Delete the entity with given eid."""
        pass

    @abstractmethod
    def delete(self, entity: T) -> None:
        """Delete the given entity."""
        pass

    @abstractmethod
    def delete_all_by_eids(self, ids: List[int]) -> None:
        """Delete all entities with given eids."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Delete all entities, managed by this repository."""
        pass
