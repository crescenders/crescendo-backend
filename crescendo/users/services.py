import typing as t
from abc import ABC, abstractmethod

from crescendo.users.models import User


class UserServiceABC(ABC):
    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def get_list(
        self,
        page: int,
        per_page: int,
        filter_by: t.Optional[str],
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
    def withdraw(self):
        pass


class UserService(UserServiceABC):
    """회원정보조회, 회원가입, 회원정보수정, 회원탈퇴, 검색"""

    def __init__(self, model: t.Type[User]):
        self.model = model

    def register(self):
        pass

    def get_list(
        self,
        page: int,
        per_page: int,
        filter_by: t.Optional[str],
        ordering: str,
    ):
        query = User.query
        # 검색어가 있을 경우 처리
        if filter_by:
            filter_by = f"%%{filter_by}%%"
            query = query.filter(
                # username, email 에 검색어가 포함되어 있다면 결과에 나타남
                User.username.ilike(filter_by)
                | User.email.ilike(filter_by)
            )
        # 정렬 조건 처리, 기본값은 내림차순인 "desc"
        if ordering == "desc":
            query = query.order_by(User.id.desc())
        elif ordering == "asc":
            query = query.order_by(User.id.asc())
        # 페이지네이션 처리
        query = query.paginate(
            page=page, per_page=per_page, count=True, error_out=False
        )

        return dict(
            total=query.total,
            current_page=query.page,
            total_page=query.pages,
            has_prev=query.has_prev,
            has_next=query.has_next,
            users=query.items,
        )

    def get_one(self):
        pass

    def edit_info(self):
        pass

    def withdraw(self):
        pass
