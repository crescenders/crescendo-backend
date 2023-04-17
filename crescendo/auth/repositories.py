from abc import ABC, abstractmethod
from typing import Optional

from flask_sqlalchemy import Pagination
from flask_sqlalchemy.query import Query

from core.entities.pagination import PaginationEntity
from core.extensions import db
from crescendo.auth.entities import UserEntity
from crescendo.auth.models import UserModel


class UserRepositoryABC(ABC):
    @abstractmethod
    def read_one_by_uuid(self, uuid: str) -> UserEntity:
        pass

    @abstractmethod
    def read_one_by_email(self, email: str) -> UserEntity:
        pass

    @abstractmethod
    def read_list(self, page: int, per_page: int, filter_by: str, ordering: str):
        pass

    @abstractmethod
    def delete(self, model):
        pass

    @abstractmethod
    def save(self, model):
        pass


class SQLAlchemyUserRepository(UserRepositoryABC):
    def __init__(self, user_model_cls, pagination_entity_factory, user_entity_factory):
        self.user_model_cls = user_model_cls
        self.pagination_entity_factory = pagination_entity_factory
        self.user_entity_factory = user_entity_factory

    def read_one_by_uuid(self, uuid) -> UserEntity:
        """
        UUID 로 특정할 수 있는 사용자 정보를 조회합니다.

        :param uuid: 사용자 UUID
        :return:
        """
        return self.user_model_cls.query.filter_by(uuid=uuid).first()

    def read_one_by_email(self, email: str) -> UserEntity:
        """
        email 로 특정할 수 있는 사용자 정보를 조회합니다.

        :param email: 사용자 email
        :return:
        """
        return self.user_model_cls.query.filter_by(email=email).first()

    def read_list(
        self, page: int, per_page: int, filter_by: Optional[str], ordering: str
    ) -> PaginationEntity:
        """
        페이지네이션, 필터링, 정렬조건을 적용하여 사용자의 목록을 반환합니다.

        :param page:
        :param per_page:
        :param filter_by:
        :param ordering: 정렬 조건
        :return:
        """
        query = self._get_base_query()

        if filter_by:
            query = self._filter_by(query, filter_by)

        query = self._order_by(query, ordering)
        result = self._paginate(query, page, per_page)
        return self.pagination_entity_factory(
            count=result.total,
            next=result.next_num,
            previous=result.prev_num,
            results=result.items,
        )

    def delete(self, model: UserModel) -> UserEntity:
        """UserEntity 객체를 데이터베이스에서 삭제합니다."""
        with db.session.begin():
            db.session.add(model)
        return model

    def save(self, model: UserModel) -> UserEntity:
        """UserEntity 객체를 데이터베이스에서 저장합니다."""
        with db.session.begin():
            db.session.add(model)
        return model

    def _get_base_query(self) -> Query:
        """SQLAlchemy Query 객체를 생성합니다."""
        return self.user_model_cls.query

    def _filter_by(self, query: Query, filter_by: str) -> Query:
        """
        SQLAlchemy Query 객체에 필터 조건을 추가합니다.

        :param query: SQLAlchemy Query 객체
        :param filter_by: 검색어
        :return: 필터링이 완료된 SQLAlchemy Query 객체
        """
        filter_by = f"%%{filter_by}%%"
        return query.filter(
            self.user_model_cls.username.ilike(filter_by)
            | self.user_model_cls.email.ilike(filter_by)
        )

    def _order_by(self, query: Query, ordering: str) -> Query:
        """
        SQLAlchemy Query 객체에 정렬 조건을 추가합니다.

        :param query: SQLAlchemy Query 객체
        :param ordering: 정렬 조건
        :return: SQLAlchemy 의 Query 객체
        """
        if ordering == "desc":
            return query.order_by(self.user_model_cls.id.desc())
        elif ordering == "asc":
            return query.order_by(self.user_model_cls.id.asc())
        else:
            return query

    def _paginate(self, query: Query, page: int, per_page: int) -> Pagination:
        """
        SQLAlchemy Pagination 을 진행합니다.

        :param query: SQLAlchemy Query 객체
        :param page: 조회하고자 하는 페이지 번호
        :param per_page: 한 페이지에 들어갈 아이템 갯수
        :return: SQLAlchemy 의 Pagination 객체
        """
        return query.paginate(page=page, per_page=per_page, count=True, error_out=False)
