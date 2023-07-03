from abc import ABC, abstractmethod

from crescendo.exceptions.service_exceptions import DataNotFound
from crescendo.study.models import CategoryModel
from crescendo.study.repositories import SQLAlchemyFullCategoryRepositoryABC


class CategoryServiceABC(ABC):
    @abstractmethod
    def create(self, category_category_data):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def edit(self, category_id, category_data):
        pass

    @abstractmethod
    def delete(self, category_id):
        pass


class CategoryService(CategoryServiceABC):
    def __init__(self, category_repository: SQLAlchemyFullCategoryRepositoryABC):
        self.category_repository = category_repository

    def create(self, category_data):
        new_category = self.category_repository.save(CategoryModel(**category_data))
        return new_category

    def get_all(self):
        return self.category_repository.read_all()

    def edit(self, category_id, category_data):
        category = self.category_repository.read_by_id(category_id)
        if category is None:
            raise DataNotFound
        category.name = category_data["name"]
        category.description = category_data["description"]
        return self.category_repository.save(category)

    def delete(self, category_id):
        category = self.category_repository.read_by_id(category_id)
        if category is None:
            raise DataNotFound
        return self.category_repository.delete(category)
