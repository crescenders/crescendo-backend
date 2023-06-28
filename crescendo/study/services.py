from abc import ABC, abstractmethod


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
    def create(self):
        pass

    def get_all(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass
