from abc import ABC, abstractmethod

from crescendo.users.models import User


class UserServiceABC(ABC):
    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def get_lists(self):
        pass

    @abstractmethod
    def get_one(self):
        pass

    @abstractmethod
    def edit_info(self):
        pass

    @abstractmethod
    def withdraw(self):
        pass


class UserService(UserServiceABC):
    """회원정보조회, 회원가입, 회원정보수정, 회원탈퇴, 검색"""

    def register(self):
        pass

    def get_lists(self):
        pass

    def get_one(self):
        pass

    def edit_info(self):
        pass

    def withdraw(self):
        pass
