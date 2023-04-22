"""
auth 앱의 resources.py (presentation layer) 를 테스트합니다.
"""
from unittest import mock

import pytest
from flask import url_for

from app import create_app
from crescendo.auth.services import UserServiceABC


@pytest.fixture
def test_app():
    test_app = create_app()
    yield test_app
    test_app.user_container.unwire()


def test_user_list_api_without_jwt_should_401(test_app):
    """
    사용자 목록을 다루는 API 에서, 로그인이 필요하지만 JWT 를 제공하지 않은 경우
    서버가 적절한 응답을 하는지를 테스트합니다.

    JWT가 HTTP 헤더에 담겨있지 않으면,
    서버는 HTTP 401 상태 코드를 반환해야 합니다.
    """
    user_service = mock.Mock(spec=UserServiceABC)
    user_service.get_list.return_value = None

    with test_app.test_request_context():
        with test_app.user_container.user_service.override(user_service):
            response = test_app.test_client().get(url_for("AuthAPI.UserListAPI"))
    assert response.status_code == 401


def test_user_list_api_invalid_parameters_should_422(test_app):
    """
    사용자 목록 조회 API 에서, 클라이언트의 GET parameter 를
    적절하게 검증하는지 테스트합니다.

    적절하지 않은 paramter 로 요청이 들어오면,
    서버는 HTTP 422 상태 코드를 반환해야 합니다.
    """

    invalid_query_parameters = {
        "per_page": 1,
        "page": 2,
        "ordering": "something_invalid",  # 적절하지 않은 parameter
        "filter_by": None,
    }

    user_service = mock.Mock(spec=UserServiceABC)
    user_service.get_list.return_value = None

    with test_app.test_request_context():
        with test_app.user_container.user_service.override(user_service):
            response = test_app.test_client().get(
                url_for("AuthAPI.UserListAPI", **invalid_query_parameters)
            )
    assert response.status_code == 422


def test_user_list_api_ordering_should_success(test_app):
    """ """
    pass
