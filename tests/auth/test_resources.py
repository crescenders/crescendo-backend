# """
# auth 앱의 resources.py (presentation layer) 를 테스트합니다.
# """
#
# import pytest
#
# from app import CrescendoApplicationFactory
#
#
# @pytest.fixture
# def test_app():
#     test_app = CrescendoApplicationFactory.create_app()
#     yield test_app
#     test_app.user_container.unwire()
