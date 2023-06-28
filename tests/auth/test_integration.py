"""
auth 앱의 모든 레이어가 정상적으로 결합하여 동작하는지 테스트합니다.
"""
import os

import pytest
from flask import url_for

from crescendo.auth.models import UserModel
from factory import CrescendoApplicationFactory


@pytest.fixture
def test_app_factory():
    os.environ["SECRET_KEY"] = ""
    yield CrescendoApplicationFactory


@pytest.fixture
def test_app(test_app_factory):
    test_app = test_app_factory.create_app("test")
    with test_app.app_context():
        UserModel
        db = test_app_factory.get_extensions().db
        db.create_all()
        db.session.add(
            UserModel(username="react", email="user_react@react.com")
        )  # id == 1
        db.session.add(
            UserModel(username="django", email="user_django@django.com")
        )  # id == 2
        db.session.add(
            UserModel(username="flask", email="user_flask@flask.com")
        )  # id == 3
        db.session.add(
            UserModel(username="fastapi", email="user_fastapi@fastapi.com")
        )  # id == 4
        db.session.commit()
    yield test_app
    with test_app.app_context():
        db = test_app_factory.get_extensions().db
        db.drop_all()


def test_user_list_api(test_app):
    """
    쿼리 파라미터가 없는 사용자 목록 조회 API 를 테스트합니다.
    """
    with test_app.test_request_context():
        response = test_app.test_client().get(url_for("AuthAPI.UserListAPI"))
        assert response.status_code == 200
        assert len(response.json) == 4


def test_user_detail_get_api_return_404(test_app):
    """
    데이터베이스에 존재하지 않는 사용자 UUID 로 사용자 조회를 하려고 한다면,
    API 는 상태 코드 404를 응답해야 합니다.
    """
    with test_app.test_request_context():
        response = test_app.test_client().get(
            url_for("AuthAPI.UserDetailAPI", user_uuid="aaa")
        )
        assert response.status_code == 404


def test_user_detail_get_api_return_200(test_app):
    """
    데이터베이스에 존재하는 사용자 UUID 로 사용자 조회를 하려고 한다면,
    정상적으로 조회가 되어야 합니다.
    """
    with test_app.test_request_context():
        uuid = UserModel.query.first().uuid
        response = test_app.test_client().get(
            url_for("AuthAPI.UserDetailAPI", user_uuid=uuid)
        )
        assert response.json.get("username") == "react"
        assert response.status_code == 200


def test_user_detail_put_api_return_404(test_app):
    """
    데이터베이스에 존재하지 않는 사용자 UUID 로 사용자 정보를 수정하려고 한다면,
    API 는 상태 코드 404를 응답해야 합니다.
    """
    with test_app.test_request_context():
        response = test_app.test_client().put(
            url_for("AuthAPI.UserDetailAPI", user_uuid="invalid_uuid")
        )
        assert response.status_code == 404


def test_user_detail_put_api_return_400(test_app):
    """
    PUT request 를 아무런 body 없이 수행한다면,
    API 는 상태 코드 400을 응답해야 합니다.
    """
    with test_app.test_request_context():
        uuid = UserModel.query.first().uuid
        response = test_app.test_client().put(
            url_for("AuthAPI.UserDetailAPI", user_uuid=uuid)
        )
        assert response.status_code == 400


def test_user_detail_put_api_return_200(test_app):
    """
    데이터베이스에 존재하는 사용자 UUID와 적절한 정보로 사용자 정보를 수정하려고 한다면,
    정상적으로 수정이 되어야 합니다.
    """
    json = {"username": "수정된_사용자명"}
    with test_app.test_request_context():
        uuid = UserModel.query.first().uuid
        response = test_app.test_client().put(
            url_for("AuthAPI.UserDetailAPI", user_uuid=uuid), json=json
        )
        assert response.json["username"] == json["username"]
        assert UserModel.query.filter_by(uuid=uuid).first().username == json["username"]
        assert response.status_code == 200


def test_user_detail_delete_api_return_404(test_app):
    """
    데이터베이스에 존재하지 않는 사용자 UUID 로 사용자 정보를 삭제하려고 한다면,
    API 는 상태 코드 404를 응답해야 합니다.
    """
    with test_app.test_request_context():
        response = test_app.test_client().delete(
            url_for("AuthAPI.UserDetailAPI", user_uuid="invalid_uuid")
        )
        assert response.status_code == 404


def test_user_detail_delete_api_return_204(test_app):
    """
    데이터베이스에 존재하지 않는 사용자 UUID 로 사용자 정보를 삭제하려고 한다면,
    API 는 상태 코드 404를 응답해야 합니다.
    """
    with test_app.test_request_context():
        uuid = UserModel.query.first().uuid
        response = test_app.test_client().delete(
            url_for("AuthAPI.UserDetailAPI", user_uuid=uuid)
        )
        assert response.status_code == 204
        assert len(UserModel.query.all()) == 3
