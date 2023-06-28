from abc import ABC, abstractmethod

from crescendo.study.repositories import SQLAlchemyFullCategoryRepositoryABC


class CategoryServiceABC(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def edit(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class CategoryService(CategoryServiceABC):
    def __init__(self, category_repository: SQLAlchemyFullCategoryRepositoryABC):
        self.category_repository = category_repository

    def create(self):
        pass

    def get_all(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass
