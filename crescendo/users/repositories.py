from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from flask_sqlalchemy.pagination import QueryPagination
from flask_sqlalchemy.query import Query

from core.extensions import db
from crescendo.users.models import UserModel


class UserRepositoryABC(ABC):
    @abstractmethod
    def read_one_by_uuid(self, uuid: str):
        pass

    @abstractmethod
    def read_list(
        self, page: int, per_page: int, filter_by: str, ordering: str
    ) -> dict[str, int | list[Any]]:
        pass

    @abstractmethod
    def delete(self, model):
        pass

    @abstractmethod
    def save(self, model):
        pass


class UserRepository(UserRepositoryABC):
    def __init__(self):
        self.user_model = UserModel

    def _get_base_query(self) -> Query:
        return self.user_model.query

    def read_one_by_uuid(self, uuid) -> Optional[UserModel]:
        return self.user_model.query.filter_by(uuid=uuid).first()

    def read_list(
        self, page: int, per_page: int, filter_by: Optional[str], ordering: str
    ) -> dict[str, int | list[Any]]:
        query = self._get_base_query()

        if filter_by:
            query = self._filter_by(query, filter_by)

        query = self._order_by(query, ordering)
        result = self._paginate(query, page, per_page)
        return dict(
            current_page=result.page,
            per_page=result.per_page,
            total_page=result.pages,
            results=result.items,
        )

    def _filter_by(self, query: Query, filter_by: str) -> Query:
        filter_by = f"%%{filter_by}%%"
        return query.filter(
            self.user_model.username.ilike(filter_by)
            | self.user_model.email.ilike(filter_by)
        )

    def _order_by(self, query: Query, ordering: str) -> Query:
        if ordering == "desc":
            return query.order_by(self.user_model.id.desc())
        elif ordering == "asc":
            return query.order_by(self.user_model.id.asc())
        else:
            return query

    def _paginate(self, query: Query, page: int, per_page: int) -> QueryPagination:
        return query.paginate(page=page, per_page=per_page, count=True, error_out=False)

    def delete(self, model: UserModel) -> UserModel:
        with db.session.begin():
            db.session.add(model)
        return model

    def save(self, model: UserModel) -> UserModel:
        with db.session.begin():
            db.session.add(model)
        return model
