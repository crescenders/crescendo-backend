from abc import ABC, abstractmethod
from typing import Optional

from core.repositories.sqlalchemy import SQLAlchemyFullRepository
from crescendo.auth.entities import UserEntity


class SQLAlchemyFullUserRepositoryABC(SQLAlchemyFullRepository, ABC):
    @abstractmethod
    def read_by_uuid(self, uuid: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def read_by_email(self, email: str) -> Optional[UserEntity]:
        pass


class SQLAlchemyFullUserRepository(SQLAlchemyFullUserRepositoryABC):
    def read_by_uuid(self, uuid: str) -> Optional[UserEntity]:
        query_result = self.sqlalchemy_model.query.filter_by(uuid=uuid).first()
        if query_result:
            return self._sqlalchemy_model_to_entity(query_result)
        return None

    def read_by_email(self, email: str) -> Optional[UserEntity]:
        query_result = self.sqlalchemy_model.query.filter_by(email=email).first()
        if query_result:
            return self._sqlalchemy_model_to_entity(query_result)
        return None
