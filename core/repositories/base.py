from typing import Type

from core.entities.base_entity import BaseEntity


class BaseRepository:
    """
    The Base Repository class of all Repositories.
    """

    def __init__(self, entity: Type[BaseEntity]):
        """
        :param entity: The types of entities you want to cover in this repository.
        """
        self.entity = entity
