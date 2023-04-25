from typing import Generic, Type

from core.repositories.type import T


class BaseRepository(Generic[T]):
    """
    The Base Repository class of all Repositories.
    """

    def __init__(self, entity: Type[T]):
        """
        :param entity: The types of entities you want to cover in this repository.
        """
        self.entity = entity
