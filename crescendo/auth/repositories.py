from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

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
    # TODO : legacy query 대응 방안 알아보기
    def read_by_uuid(self, uuid: UUID) -> Optional[UserEntity]:
        return self.sqlalchemy_model.query.filter_by(uuid=str(uuid)).first()

    def read_by_email(self, email: str) -> Optional[UserEntity]:
        return self.sqlalchemy_model.query.filter_by(email=str(email)).first()
