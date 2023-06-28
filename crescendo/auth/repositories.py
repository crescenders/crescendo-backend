from abc import ABC, abstractmethod
from typing import Optional

from fullask_rest_framework.repositories.sqlalchemy import (
    SQLAlchemyFullRepository,
    read_by_fields,
)

from crescendo.auth.entities import UserEntity


class FullUserRepositoryABC(SQLAlchemyFullRepository, ABC):
    @abstractmethod
    def read_by_uuid(self, uuid: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def read_by_email(self, email: str) -> Optional[UserEntity]:
        pass


class FullUserRepository(FullUserRepositoryABC):
    ENTITY_CLS = UserEntity

    @read_by_fields
    def read_by_uuid(self, uuid: str) -> Optional[UserEntity]:
        pass

    @read_by_fields
    def read_by_email(self, email: str) -> Optional[UserEntity]:
        pass
