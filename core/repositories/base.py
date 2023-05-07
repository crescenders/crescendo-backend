from typing import Generic, Type


class BaseRepository:
    """
    The Base Repository class of all Repositories.
    """

    def __init__(self, entity):
        """
        :param entity: The types of entities you want to cover in this repository.
        """
        self.entity = entity
