from typing import Generic, List, Optional

from flask_marshmallow.sqla import SQLAlchemyAutoSchema  # type: ignore[import]
from flask_sqlalchemy.query import Query
from sqlalchemy import inspect, or_, select

from core.entities.filtering import FilteringRequest
from core.entities.pagination import PaginationRequest, PaginationResponse
from core.repositories.base import T
from core.repositories.crud import CRUDRepositoryABC


class SQLAlchemyFullRepository(CRUDRepositoryABC, Generic[T]):
    """
    The implementation of CRUDRepositoryABC, with SQLAlchemy.

    this implementation has dependency with flask-sqlalchemy's SQLAlchemy object.
    """

    def __init__(self, entity, db, sqlalchemy_model):
        """
        :param db: flask-sqlalchemy.SQLAlchemy
        :param sqlalchemy_model: the SQLAlchemy model
        """
        self.db = db
        self.sqlalchemy_model = sqlalchemy_model
        super().__init__(entity=entity)
        assert set(self.entity.__annotations__.keys()) == set(
            [column.name for column in self.sqlalchemy_model.__table__.columns]
        ), (
            "sqlalchemy model fields not match entity fields."
            f"{self.entity.__annotations__.keys()} "
            f"!= "
            f"{[column.name for column in self.sqlalchemy_model.__table__.columns]}"
        )

    def save(self, entity: T) -> T:
        model_instance = self._entity_to_sqlalchemy_model(entity)
        with self.db.session.begin():
            self.db.session.add(model_instance)
        self.db.session.refresh(model_instance)
        return self._sqlalchemy_model_to_entity(model_instance)

    def save_all(self, entities: List[T]) -> List[T]:
        model_instances = [
            self._entity_to_sqlalchemy_model(entity) for entity in entities
        ]
        with self.db.session.begin():
            for model_instance in model_instances:
                self.db.session.add(model_instance)
            self.db.session.commit()
        for model_instance in model_instances:
            self.db.session.refresh(model_instance)
        return [
            self._sqlalchemy_model_to_entity(model_instance)
            for model_instance in model_instances
        ]

    def read_by_id(self, id: int) -> Optional[T]:
        query_result = self.db.session.get(self.sqlalchemy_model, id)
        if query_result:
            return self._sqlalchemy_model_to_entity(query_result)
        return None

    def is_exists_by_id(self, id) -> bool:
        if id is None:
            raise ValueError("id cannot be None.")
        return bool(self.db.session.get(self.sqlalchemy_model, id))

    def read_all(
        self,
        sorting_request=None,
        filtering_request=None,
    ) -> List[Optional[T]]:
        query = self._get_base_query()
        # TODO : Add Filtering and Sorting
        if filtering_request:
            pass
        if sorting_request:
            pass
        else:
            # if no pagination request, return all results without pagination.
            return [
                self._sqlalchemy_model_to_entity(query_result)
                for query_result in self.db.session.execute(
                    select(self.sqlalchemy_model)
                )
                .scalars()
                .all()
            ]

    def read_all_with_pagination(
        self,
        pagination_request: PaginationRequest,
        sorting_request=None,
        filtering_request=None,
    ) -> PaginationResponse[T]:
        # TODO: 테스트 코드 작성, filtering and sorting 처리
        query = self._get_base_query()
        if filtering_request:
            # TODO : 구현하기
            query = self._filtering(query=query, filtering_request=filtering_request)
        if sorting_request:
            # TODO : 구현하기
            query = self._sorting(query=query)
        query = self._get_base_query().paginate(
            page=pagination_request.page,
            per_page=pagination_request.per_page,
        )
        return PaginationResponse(
            count=query.total,
            next_page=query.next_num,
            previous_page=query.prev_num,
            results=[self._sqlalchemy_model_to_entity(item) for item in query.items],
        )

    def read_all_by_ids(self, ids: List[int]) -> List[Optional[T]]:
        return [self.read_by_id(_id) for _id in ids]

    def count(self) -> int:
        return self.db.session.query(self.sqlalchemy_model).count()

    def delete_by_id(self, id: int) -> None:
        model_instance = self.db.session.get(self.sqlalchemy_model, id)
        if model_instance:
            self.db.session.delete(self.db.session.get(self.sqlalchemy_model, id))
            self.db.session.commit()
        else:
            raise ValueError(f"{self.sqlalchemy_model} with id {id} not found.")

    def delete(self, entity) -> None:
        model_instance = self.db.session.get(self.sqlalchemy_model, entity.id)
        if not model_instance:
            raise ValueError(
                f"{self.sqlalchemy_model} with entity {entity} not found.\n"
                f"make sure the entity instance is stored in database."
            )
        self.db.session.delete(model_instance)
        self.db.session.commit()

    def delete_all_by_ids(self, ids: List[int]) -> None:
        self.db.session.query(self.sqlalchemy_model).filter(
            self.sqlalchemy_model.id.in_(ids)
        ).delete()

    def delete_all(self) -> None:
        self.sqlalchemy_model.query.delete()

    def _get_base_query(self) -> Query:
        return self.db.session.query(self.sqlalchemy_model)

    def _filtering(self, query: Query, filtering_request: FilteringRequest) -> Query:
        for field, word in vars(filtering_request).items():
            query = query.filter(
                getattr(self.sqlalchemy_model, field).ilike(f"%{word}%")
            )
        return query

    def _sorting(self, query: Query, sorting_request: dict) -> Query:
        # TODO : 구현하기
        pass

    def _sqlalchemy_model_to_entity(self, sqlalchemy_instance) -> T:
        assert isinstance(
            sqlalchemy_instance, self.sqlalchemy_model
        ), f"{sqlalchemy_instance} is not {self.sqlalchemy_model}"
        sqlalchemy_model_pk_names = [
            pk.name for pk in inspect(self.sqlalchemy_model).primary_key
        ]
        if len(sqlalchemy_model_pk_names) == 1:
            instance_dict = sqlalchemy_instance.__dict__
            instance_dict.pop("_sa_instance_state")
            return self.entity(**instance_dict)
        else:
            raise ValueError("multi-pk case is not supported in current version.")
            # TODO : handle multi-pk case

    def _entity_to_sqlalchemy_model(self, entity):
        assert isinstance(
            entity, self.entity
        ), f"{entity} is not instance of {self.entity}"
        return self.sqlalchemy_model(**self._get_sqlalchemy_schema().dump(entity))

    def _get_sqlalchemy_schema(self) -> SQLAlchemyAutoSchema:
        class SQLAlchemyModelSchema(SQLAlchemyAutoSchema):
            class Meta:
                model = self.sqlalchemy_model

        return SQLAlchemyModelSchema()
