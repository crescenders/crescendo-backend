"""
auth 앱의 resources.py (presentation layer) 를 테스트합니다.
"""


from unittest import mock

import pytest
from flask import url_for

from app import create_app
from core.entities.pagination import PaginationEntity
from crescendo.auth.entities import UserEntity
from crescendo.auth.services import UserServiceABC


@pytest.fixture
def test_app():
    test_app = create_app()
    yield test_app
    test_app.user_container.unwire()


def test_user_list_api_invalid_parameters_should_400(test_app):
    """
    Presentation Layer 에서, 클라이언트의 GET parameter 를
    적절하게 검증하는지 테스트합니다.

    적절하지 않은 paramter 로 요청이 들어오면,
    서버는 HTTP 400 상태 코드를 반환해야 합니다.
    """

    # 적절하지 않은 parameter 정의
    invalid_query_parameters = {
        "per_page": 1,
        "page": 2,
        "ordering": "desc",
        "filter_by": None,
        "Ye": "BuddY!",  ## Error?
    }

    # service layer Mocking
    user_service = mock.Mock(spec=UserServiceABC)
    user_service.get_list.return_value = None

    with test_app.test_request_context():
        with test_app.user_container.user_service.override(user_service):
            response = test_app.test_client().get(
                url_for("AuthAPI.UserListAPI", **invalid_query_parameters)
            )
    assert response.status_code == 400
