from abc import ABC, abstractmethod
from typing import Optional

from fullask_rest_framework.repositories.sqlalchemy import SQLAlchemyFullRepository


class SQLAlchemyFullCategoryRepositoryABC(SQLAlchemyFullRepository, ABC):
    pass


class SQLAlchemyFullCategoryRepository(SQLAlchemyFullCategoryRepositoryABC):
    pass
