from typing import Generic, Type

from core.repositories.type import DBEntity


class BaseRepository(Generic[DBEntity]):
    """
    The Base Repository class of all Repositories.
    """

    def __init__(self, entity: Type[DBEntity]):
        """
        :param entity: The types of entities you want to cover in this repository.
        """
        self.entity = entity
