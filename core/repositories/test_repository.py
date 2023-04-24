import pytest

from core.extensions import db
from core.factory import create_app
from core.repositories.sqla import SQLAlchemyRepositoryABC
from crescendo.auth.entities import UserEntity
from crescendo.auth.models import UserModel


@pytest.fixture
def test_app():
    test_app = create_app()
    yield test_app
    test_app.user_container.unwire()


def test_repository_read_by_eid_success(test_app):
    with test_app.test_request_context():
        sqlalchemy_model = UserModel
        user = SQLAlchemyRepositoryABC(
            UserEntity, db=db, sqlalchemy_model=sqlalchemy_model
        ).read_by_id(1)
    assert isinstance(user, UserEntity)
    assert user.id == 1
