import os

import pytest
from flask import url_for

from crescendo.study.models import CategoryModel
from factory import CrescendoApplicationFactory


@pytest.fixture
def test_app_factory():
    os.environ["SECRET_KEY"] = ""
    yield CrescendoApplicationFactory


@pytest.fixture
def test_app(test_app_factory):
    test_app = test_app_factory.create_app("test")
    with test_app.app_context():
        CategoryModel
        db = test_app_factory.get_extensions().db
        db.create_all()
        db.session.add(
            CategoryModel(name="backend", description="backend category")
        )  # id == 1
        db.session.add(
            CategoryModel(name="frontend", description="frontend category")
        )  # id == 2
        db.session.commit()
    yield test_app
    with test_app.app_context():
        db = test_app_factory.get_extensions().db
        db.drop_all()


def test_category_list_api(test_app):
    """
    카테고리 조회 api 를 테스트합니다.
    미리 만들어 둔 2개의 카테고리가 잘 조회되어야 합니다.
    """
    with test_app.test_request_context():
        response = test_app.test_client().get(url_for("CategoryAPI.CategoryListAPI"))
        assert response.status_code == 200
        assert len(response.json) == 2


def test_category_detail_put_api_return_404(test_app):
    """
    데이터베이스에 존재하지 않는 카테고리 ID 로 카테고리 정보를 수정하려고 한다면,
    API 는 상태 코드 404를 응답해야 합니다.
    """
    json = {"name": "수정된_카테고리", "description": "수정된_설명"}
    with test_app.test_request_context():
        response = test_app.test_client().put(
            url_for("CategoryAPI.CategoryDetailAPI", category_id=3), json=json
        )
        assert response.status_code == 404


def test_category_detail_put_api_return_422(test_app):
    """
    PUT request 를 아무런 body 없이 수행한다면,
    API 는 상태 코드 422을 응답해야 합니다.
    """
    with test_app.test_request_context():
        category_id = CategoryModel.query.first().id
        response = test_app.test_client().put(
            url_for("CategoryAPI.CategoryDetailAPI", category_id=category_id)
        )
        assert response.status_code == 422


def test_category_detail_put_api_return_200(test_app):
    """
    데이터베이스에 존재하는 카테고리 ID와 적절한 body로 정보를 수정하려고 한다면,
    정상적으로 수정이 되어야 합니다.
    """
    json = {"name": "수정된_카테고리", "description": "수정된_설명"}
    with test_app.test_request_context():
        category_id = CategoryModel.query.first().id
        response = test_app.test_client().put(
            url_for("CategoryAPI.CategoryDetailAPI", category_id=category_id), json=json
        )
        print("--------------------")
        print(response.json)
        # assert response.json["name"] == json["name"]
        assert (
            CategoryModel.query.filter_by(id=category_id).first().name == json["name"]
        )
        assert response.status_code == 200


def test_category_detail_delete_api_return_404(test_app):
    """
    데이터베이스에 존재하지 않는 카테고리 ID 로 카테고리를 삭제하려고 한다면,
    API 는 상태 코드 404를 응답해야 합니다.
    """
    with test_app.test_request_context():
        response = test_app.test_client().delete(
            url_for("CategoryAPI.CategoryDetailAPI", category_id=6)
        )
        assert response.status_code == 404


def test_category_detail_delete_api_return_204(test_app):
    """
    데이터베이스에 존재하는 카테고리 ID 로 카테고리를 삭제하려고 한다면, 정상적으로 삭제가 수행되어야 합니다.
    """
    with test_app.test_request_context():
        category_id = CategoryModel.query.first().id
        response = test_app.test_client().delete(
            url_for("CategoryAPI.CategoryDetailAPI", category_id=category_id)
        )
        assert response.status_code == 204
        assert len(CategoryModel.query.all()) == 1
