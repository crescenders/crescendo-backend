from abc import ABC

from fullask_rest_framework.repositories import SQLAlchemyFullRepository

from crescendo.study.models import CategoryModel


class CategoryRepositoryABC(SQLAlchemyFullRepository, ABC):
    pass


class CategoryRepository(CategoryRepositoryABC):
    def get_model(self):
        return CategoryModel
