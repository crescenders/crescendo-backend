from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from core.entities.pagination import PaginationResponse
from core.repositories.base import BaseRepository


class CRUDRepositoryABC(BaseRepository, ABC):
    """The Base CRUD Repository class."""

    @abstractmethod
    def save(self, entity):
        """
        Save the given entity.

        :param entity: Entity to save.
        :return: saved Entity
        """
        pass

    @abstractmethod
    def save_all(self, entities):
        """
        Save all given entities.

        :param entities: Entities to save.
        :return: saved Entities.
        """
        pass

    @abstractmethod
    def read_by_id(self, id: int):
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
    def read_all(self, sorting_request: dict, filtering_request: dict):
        """
        Read all entities.
        if no entities are found, return empty list.
        """
        pass

    @abstractmethod
    def read_all_with_pagination(
        self, pagination_request: dict, sorting_request: dict, filtering_request: dict
    ) -> PaginationResponse:
        """
        Read all entities with pagination.
        if no entities are found, return empty list.
        """
        pass

    @abstractmethod
    def read_all_by_ids(self, ids: List[int]):
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
    def delete(self, entity) -> None:
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
