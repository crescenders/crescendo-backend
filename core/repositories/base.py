from typing import Generic, Type

from core.repositories.type import T


class BaseRepository(Generic[T]):
    """
    The Base Repository class of all Repositories.
    """

    def __init__(self, entity: Type[T], eid_name: str):
        """
        :param entity: The types of entities you want to cover in this repository
        :param eid_name: Primary key name in Entity
        """
        self.entity = entity
        self.eid_name = eid_name
