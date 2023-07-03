from abc import ABC

from fullask_rest_framework.repositories.sqlalchemy import SQLAlchemyFullRepository

from crescendo.study.models import CategoryModel


class SQLAlchemyFullCategoryRepositoryABC(SQLAlchemyFullRepository, ABC):
    pass


class SQLAlchemyFullCategoryRepository(SQLAlchemyFullCategoryRepositoryABC):
    def get_model(self):
        return CategoryModel
