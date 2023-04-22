from typing import List, Optional, Type

from flask_sqlalchemy import SQLAlchemy

from core.repositories.crud import CRUDRepositoryABC
from core.repositories.type import T


class SQLAlchemyRepositoryABC(CRUDRepositoryABC):
    """
    The implementation of CRUDRepositoryABC, with SQLAlchemy.

    this implementation has dependency with flask-sqlalchemy's SQLAlchemy object.
    """

    def __init__(
        self, entity: Type[T], eid_name: str, db: SQLAlchemy, sqlalchemy_model
    ):
        """
        :type db: flask-sqlalchemy.SQLAlchemy
        :param sqlalchemy_model: the SQLAlchemy model
        """
        self.db = db
        self.sqlalchemy_model = sqlalchemy_model
        super().__init__(entity, eid_name)

    def save(self, entity: T) -> T:
        with self.db.session.begin():
            self.db.session.add(self._entity_to_model(self.entity))

    def save_all(self, entities: List[T]) -> List[T]:
        pass

    def read_by_eid(self) -> Optional[T]:
        pass

    def is_exists_by_eid(self) -> bool:
        pass

    def read_all(self) -> List[T]:
        pass

    def read_all_by_eids(self, ids: List[int]) -> List[T]:
        pass

    def count(self) -> int:
        pass

    def delete_by_eid(self, eid: int) -> None:
        pass

    def delete(self, entity: T) -> None:
        pass

    def delete_all_by_eids(self, ids: List[int]) -> None:
        pass

    def delete_all(self) -> None:
        pass

    def _sqlalchemy_model_to_entity(self, sqlalchemy_model) -> T:
        """convert sqlalchemy model to entity."""
