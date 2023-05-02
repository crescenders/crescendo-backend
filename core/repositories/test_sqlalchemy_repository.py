from dataclasses import dataclass
from typing import Optional

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.repositories.sqlalchemy import SQLAlchemyFullRepository

###################
# pytest fixtures #
###################


db = SQLAlchemy()


class UserModel(db.Model):  # type: ignore[name-defined]
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


@dataclass
class UserEntity:
    name: str

    id: Optional[int] = None


@pytest.fixture
def test_app():
    test_app = Flask("test_app")
    test_app.config["TESTING"] = True
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db.init_app(test_app)

    with test_app.app_context():
        UserModel
        db.create_all()

    yield test_app


####################
# test code starts #
####################과


def test_save_success_and_return_entity(test_app):
    """
    save() 메서드가 저장을 잘 수행하는지를 테스트합니다.
    """
    user_fullask = UserEntity(name="mr_fullask")
    with test_app.test_request_context():
        user_entity = SQLAlchemyFullRepository(
            UserEntity, db=db, sqlalchemy_model=UserModel
        ).save(user_fullask)
        assert UserModel.query.count() == 1
        assert user_entity.id == 1
        assert user_entity.name == "mr_fullask"


def test_save_all_success_and_return_entities(test_app):
    """
    save_all() 메서드가 저장을 잘 수행하는지를 테스트합니다.
    """
    user_fullask = UserEntity(name="mr_fullask")
    user_django = UserEntity(name="mr_django")
    user_fastapi = UserEntity(name="mr_fastapi")
    with test_app.test_request_context():
        user_entities = SQLAlchemyFullRepository(
            UserEntity, db=db, sqlalchemy_model=UserModel
        ).save_all([user_fullask, user_django, user_fastapi])
        assert UserModel.query.count() == 3
        assert isinstance(user_entities, list)
        assert user_entities[0].id == 1
        assert user_entities[0].name == "mr_fullask" and isinstance(
            user_entities[0], UserEntity
        )
        assert user_entities[1].id == 2
        assert user_entities[1].name == "mr_django" and isinstance(
            user_entities[0], UserEntity
        )
        assert user_entities[2].id == 3
        assert user_entities[2].name == "mr_fastapi" and isinstance(
            user_entities[0], UserEntity
        )


def test_read_by_id_should_return_none(test_app):
    """
    없는 id 로 사용자 조회를 수행하면,
    read_by_id 는 None 을 반환해야 합니다.
    """
    with test_app.test_request_context():
        user = SQLAlchemyFullRepository(
            UserEntity, db=db, sqlalchemy_model=UserModel
        ).read_by_id(1)
    assert user is None


def test_read_by_id_should_return_user_entity(test_app):
    """
    데이터베이스 테이블에 사용자 정보가 적절하게 저장되었다면,
    read_by_id 는 UserEntity 객체를 반환해야 합니다.
    """
    # 데이터베이스에 사용자를 저장합니다.
    with test_app.test_request_context():
        db.session.add(UserModel(name="mr_fullask"))
        db.session.add(UserModel(name="mr_django"))
        db.session.commit()
        # repository 를 이용해서 확인합니다.
        user_fullask = SQLAlchemyFullRepository(
            UserEntity, db=db, sqlalchemy_model=UserModel
        ).read_by_id(1)
        user_django = SQLAlchemyFullRepository(
            UserEntity, db=db, sqlalchemy_model=UserModel
        ).read_by_id(2)
    assert user_fullask.name == "mr_fullask" and isinstance(user_fullask, UserEntity)
    assert user_django.name == "mr_django" and isinstance(user_fullask, UserEntity)


def test_is_exists_by_id_should_return_false(test_app):
    """
    해당 id 로 찾을 수 없다면 False 를 반환해야 합니다.
    """
    with test_app.test_request_context():
        assert (
            SQLAlchemyFullRepository(
                UserEntity, db=db, sqlalchemy_model=UserModel
            ).is_exists_by_id(1)
            is False
        )


def test_is_exists_by_id_should_return_true(test_app):
    """
    해당 id 로 찾을 수 있다면 True 를 반환해야 합니다.
    """
    with test_app.test_request_context():
        db.session.add(UserModel(name="mr_fullask"))
        db.session.commit()
        assert (
            SQLAlchemyFullRepository(
                UserEntity, db=db, sqlalchemy_model=UserModel
            ).is_exists_by_id(1)
            is True
        )


def test_read_all_return_empty_list(test_app):
    """
    read_all() 메서드가 데이터를 잘 읽어오는지 테스트합니다.
    데이터베이스에 아무런 사용자도 저장되어있지 않다면, read_all() 은 비어있는 리스트를 반환해야 합니다.
    """
    with test_app.test_request_context():
        read_all_result = SQLAlchemyFullRepository(
            UserEntity, db=db, sqlalchemy_model=UserModel
        ).read_all()
        assert isinstance(read_all_result, list)
        assert len(read_all_result) == 0


def test_read_all_return_filled_list(test_app):
    """
    read_all() 메서드가 데이터를 잘 읽어오는지 테스트합니다.
    데이터베이스에 두 명의 사용자가 저장되어 있다면, read_list() 는 길이가 2인 리스트여야 합니다.
    그리고, 각각의 요소는 Entity 객체여야 합니다.
    """
    with test_app.test_request_context():
        db.session.add(UserModel(name="mr_fullask"))
        db.session.add(UserModel(name="mr_django"))
        db.session.commit()
        read_all_result = SQLAlchemyFullRepository(
            UserEntity, db=db, sqlalchemy_model=UserModel
        ).read_all()
        assert isinstance(read_all_result, list)
        assert len(read_all_result) == 2
        assert read_all_result[0].name == "mr_fullask" and isinstance(
            read_all_result[0], UserEntity
        )
        assert read_all_result[1].name == "mr_django" and isinstance(
            read_all_result[1], UserEntity
        )


def test_read_all_by_ids(test_app):
    """
    read_all_by_ids() 메서드가 데이터를 잘 읽어오는지 테스트합니다.
    """
    with test_app.test_request_context():
        db.session.add(UserModel(name="mr_fullask"))  # id should 1
        db.session.add(UserModel(name="mr_django"))  # id should 2
        db.session.add(UserModel(name="mr_spring"))  # id should 3
        db.session.commit()
        read_all_result = SQLAlchemyFullRepository(
            UserEntity, db=db, sqlalchemy_model=UserModel
        ).read_all_by_ids([1, 3])
        assert isinstance(read_all_result, list)
        assert len(read_all_result) == 2
        assert read_all_result[0].name == "mr_fullask" and isinstance(
            read_all_result[0], UserEntity
        )
        assert read_all_result[1].name == "mr_spring" and isinstance(
            read_all_result[1], UserEntity
        )


def test_count_should_return_2(test_app):
    """
    count() 메서드가 정확한 값을 리턴하는지 테스트합니다.
    사용자 2명이 저장되어 있다면, count() 메서드는 2를 반환해야 합니다.
    """
    with test_app.test_request_context():
        db.session.add(UserModel(name="mr_fullask"))
        db.session.add(UserModel(name="mr_django"))
        db.session.commit()
        assert (
            SQLAlchemyFullRepository(
                UserEntity, db=db, sqlalchemy_model=UserModel
            ).count()
            == 2
        )


def test_delete_by_id_should_success(test_app):
    """
    delete_by_id() 메서드가 id를 받아 데이터 삭제를 잘 수행하는지 테스트합니다.
    """
    with test_app.test_request_context():
        db.session.add(UserModel(name="mr_fullask"))  # id should 1
        db.session.add(UserModel(name="mr_django"))  # id should 2
        db.session.commit()
        # 삭제 전에는 사용자가 2명이어야 함
        assert db.session.query(UserModel).count() == 2
        # delete_by_id() 메서드 호출
        SQLAlchemyFullRepository(
            UserEntity, db=db, sqlalchemy_model=UserModel
        ).delete_by_id(1)
        assert db.session.query(UserModel).count() == 1


def test_delete_by_id_with_unknown_id_should_fail(test_app):
    """
    delete_by_id() 메서드가 id를 받았지만, 데이터베이스에서 해당 id로 데이터를 찾을 수 없는 경우
    ValueError 를 발생시켜야 합니다.
    """
    with test_app.test_request_context():
        with pytest.raises(ValueError):
            # delete_by_id() 메서드 호출 시에는 ValueError 가 발생해야 한다.
            SQLAlchemyFullRepository(
                UserEntity, db=db, sqlalchemy_model=UserModel
            ).delete_by_id(3)


def test_delete_by_entity_should_success(test_app):
    """
    delete() 메서드가 엔티티를 받아 데이터 삭제를 잘 수행하는지 테스트합니다.
    해당 엔티티를 데이터베이스에서 찾을 수 있다면, 삭제가 잘 이루어져야 합니다.
    """
    with test_app.test_request_context():
        # 먼저, 사용자를 저장
        db.session.add(UserModel(name="mr_fullask"))  # id is 1
        db.session.commit()

        # 삭제 전에는 사용자가 1명이어야 함
        assert db.session.query(UserModel).count() == 1

        # entity 생성
        user = UserEntity(id=1, name="mr_fullask")

        # delete() 메서드 호출, 인자로는 entity 객체가 들어옴
        SQLAlchemyFullRepository(UserEntity, db=db, sqlalchemy_model=UserModel).delete(
            entity=user
        )
        assert db.session.query(UserModel).count() == 0


def test_delete_by_invalid_entity_should_fail(test_app):
    """
    delete() 메서드가 엔티티를 받아 데이터 삭제를 잘 수행하는지 테스트합니다.
    해당 엔티티를 데이터베이스에서 찾을 수 없다면, 삭제는 실패해야 합니다.
    """
    with test_app.test_request_context():
        # 유효하지 않은 entity 생성
        invalid_user_entity = UserEntity(id=2, name="mr_fullask")

        with pytest.raises(ValueError):
            SQLAlchemyFullRepository(
                UserEntity, db=db, sqlalchemy_model=UserModel
            ).delete(invalid_user_entity)


def test_delete_by_valid_entity_should_success(test_app):
    """
    delete() 메서드가 엔티티를 받아 데이터 삭제를 잘 수행하는지 테스트합니다.
    해당 엔티티를 데이터베이스에서 찾을 수 있다면, 삭제가 잘 이루어져야 합니다.
    """
    with test_app.test_request_context():
        # 먼저, 사용자를 저장
        db.session.add(UserModel(name="mr_fullask"))
        db.session.commit()

        # 삭제 전에는 사용자가 1명이어야 함
        assert db.session.query(UserModel).count() == 1

        # 유효한 entity 생성
        valid_user_entity = UserEntity(id=1, name="mr_fullask")

        SQLAlchemyFullRepository(UserEntity, db=db, sqlalchemy_model=UserModel).delete(
            valid_user_entity
        )

        # 삭제 후에는 사용자가 0명이어야 함
        assert db.session.query(UserModel).count() == 0


def test_delete_all_by_ids_should_success(test_app):
    """
    delete_all_by_ids() 메서드가 id 를 받아 데이터 삭제를 잘 수행하는지 테스트합니다.
    받은 id가 모두 데이터베이스에 존재하고 찾을 수 있다면, 삭제가 잘 이루어져야 합니다.
    """
    with test_app.test_request_context():
        # 먼저, 사용자를 저장
        db.session.add(UserModel(name="mr_fullask"))  # id should be 1
        db.session.add(UserModel(name="mr_django"))  # id should be 2
        db.session.add(UserModel(name="mr_fastapi"))  # id should be 3
        db.session.add(UserModel(name="mr_spring"))  # id should be 4
        db.session.commit()

        SQLAlchemyFullRepository(
            UserEntity, db=db, sqlalchemy_model=UserModel
        ).delete_all_by_ids([1, 3, 4])

        assert db.session.query(UserModel).count() == 1


def test_delete_all_should_success(test_app):
    """
    delete_all() 메서드가 데이터 삭제를 잘 수행하는지 테스트합니다.
    """
    with test_app.test_request_context():
        # 먼저, 사용자를 저장
        db.session.add(UserModel(name="mr_fullask"))
        db.session.add(UserModel(name="mr_django"))
        db.session.add(UserModel(name="mr_fastapi"))
        db.session.add(UserModel(name="mr_spring"))
        db.session.commit()

        assert db.session.query(UserModel).count() == 4

        SQLAlchemyFullRepository(
            UserEntity, db=db, sqlalchemy_model=UserModel
        ).delete_all()

        assert db.session.query(UserModel).count() == 0