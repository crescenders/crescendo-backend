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
    def read_by_id(self, id) -> Optional[T]:
        """
        Read the entity with given id.

        :return: if entity is found with given id, return it, else return None
        """
        pass

    @abstractmethod
    def is_exists_by_id(self, id) -> bool:
        """
        Check if entity with given id exists.

        :return: if entity is found with given id, return True, else return False
        """
        pass

    @abstractmethod
    def read_all(self) -> List[T]:
        """
        Read all entities.
        if no entities are found, return empty list.

        :return: list of all entities.
        """
        pass

    @abstractmethod
    def read_all_by_ids(self, ids: List[int]) -> List[Optional[T]]:
        """
        Read all entities with given ids.

        :return: list of all entities, with given ids.
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """Count all entities."""
        pass

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        """Delete the entity with given id."""

        pass

    @abstractmethod
    def delete(self, entity: T) -> None:
        """Delete the given entity."""
        pass

    @abstractmethod
    def delete_all_by_ids(self, ids: List[int]) -> None:
        """Delete all entities with given ids."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Delete all entities, managed by this repository."""
        pass
