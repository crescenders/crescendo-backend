"""
auth 앱의 resources.py (presentation layer) 를 테스트합니다.
"""

import pytest

from app import CrescendoApplicationFactory


@pytest.fixture
def test_app():
    test_app = CrescendoApplicationFactory.create_app()
    yield test_app
    test_app.user_container.unwire()


# def test_user_list_api_without_jwt_should_401(test_app):
#     """
#     사용자 목록을 다루는 API 에서, 로그인이 필요하지만 JWT 를 제공하지 않은 경우
#     서버가 적절한 응답을 하는지를 테스트합니다.
#
#     JWT가 HTTP 헤더에 담겨있지 않으면,
#     서버는 HTTP 401 상태 코드를 반환해야 합니다.
#     """
#     user_service = mock.Mock(spec=UserServiceABC)
#     user_service.get_list.return_value = None
#
#     with test_app.test_request_context():
#         with test_app.user_container.user_service.override(user_service):
#             response = test_app.test_client().get(url_for("AuthAPI.UserListAPI"))
#     assert response.status_code == 401
