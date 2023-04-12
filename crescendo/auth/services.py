from abc import ABC, abstractmethod
from typing import Optional


class UserServiceABC(ABC):
    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def get_list(
        self,
        page: int,
        per_page: int,
        filter_by: Optional[str],
        ordering: str,
    ):
        pass

    @abstractmethod
    def get_one(self):
        pass

    @abstractmethod
    def edit_info(self):
        pass

    @abstractmethod
    def withdraw(self, uuid):
        pass


class UserService(UserServiceABC):
    """회원정보조회, 회원가입, 회원정보수정, 회원탈퇴, 검색"""

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register(self):
        pass

    def get_list(self, **kwargs):
        return self.user_repository.read_list(**kwargs)

    def get_one(self):
        pass

    def edit_info(self):
        pass

    def withdraw(self, uuid):
        pass
