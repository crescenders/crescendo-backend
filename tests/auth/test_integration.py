"""
auth 앱의 모든 레이어가 정상적으로 결합하여 동작하는지 테스트합니다.
"""
import os

import pytest
from flask import url_for

from factory import CrescendoApplicationFactory


@pytest.fixture
def test_app():
    os.environ["SECRET_KEY"] = ""
    test_app_factory = CrescendoApplicationFactory
    test_app = test_app_factory.create_app("test")
    with test_app.app_context():
        from crescendo.auth.models import UserModel

        test_app_factory.get_extensions().db.create_all()
    yield test_app


def test_user_list_api(test_app):
    with test_app.test_request_context():
        response = test_app.test_client().get(url_for("AuthAPI.UserListAPI"))
        assert response.status_code == 200


def test_user_detail_api(test_app):
    with test_app.test_request_context():
        # 데이터베이스에 존재하지 않는 사용자 UUID 로 사용자 조회를 하려고 한다면,
        # API 는 상태 코드 404를 응답해야 합니다.
        response = test_app.test_client().get(
            url_for("AuthAPI.UserDetailAPI", user_uuid="afsd")
        )
        assert response.status_code == 404
