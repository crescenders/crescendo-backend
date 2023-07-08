from abc import ABC, abstractmethod
from typing import Optional

from fullask_rest_framework.repositories import SQLAlchemyFullRepository, read_by_fields

from crescendo.auth.models import RoleModel, UserModel


class UserRepositoryABC(SQLAlchemyFullRepository, ABC):
    @abstractmethod
    def read_by_uuid(self, uuid: str) -> Optional[UserModel]:
        pass

    @abstractmethod
    def read_by_email(self, email: str) -> Optional[UserModel]:
        pass


class UserRepository(UserRepositoryABC):
    def get_model(self):
        return UserModel

    @read_by_fields
    def read_by_uuid(self, uuid: str) -> Optional[UserModel]:
        pass

    @read_by_fields
    def read_by_email(self, email: str) -> Optional[UserModel]:
        pass


class RoleRepositoryABC(SQLAlchemyFullRepository, ABC):
    def read_by_name(self, name):
        pass


class RoleRepository(RoleRepositoryABC):
    def get_model(self):
        return RoleModel

    @read_by_fields
    def read_by_name(self, name):
        pass
