from abc import ABC, abstractmethod
from typing import Optional

from fullask_rest_framework.repositories.sqlalchemy import SQLAlchemyFullRepository

from crescendo.study.entities import CategoryEntity


class SQLAlchemyFullCategoryRepositoryABC(SQLAlchemyFullRepository, ABC):
    pass


class SQLAlchemyFullCategoryRepository(SQLAlchemyFullCategoryRepositoryABC):
    ENTITY_CLS = CategoryEntity
