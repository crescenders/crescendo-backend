#########################
# Define your Blueprint.#
#########################
from dependency_injector.wiring import Provide, inject
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from crescendo.exceptions.service_exceptions import DataNotFound
from crescendo.study.schemas import CategoryCreateSchema, CategorySchema
from crescendo.study.services import CategoryServiceABC

category_bp = Blueprint(
    name="CategoryAPI",
    import_name=__name__,
    url_prefix="",
    description="카테고리 관리를 위한 API 입니다.",
)


@category_bp.route("/categories/")
class CategoryListAPI(MethodView):
    @inject
    def __init__(self, category_service=Provide["category_service"]):
        self.category_service = category_service

    @category_bp.response(200, CategorySchema(many=True))
    def get(self):
        """카테고리 목록을 조회합니다."""
        return self.category_service.get_all()

    @category_bp.response(201, CategorySchema())
    @category_bp.arguments(CategoryCreateSchema())
    def post(self, category_data):
        """새로운 카테고리를 생성합니다."""
        return self.category_service.create(category_data)


@category_bp.route("/categories/<int:category_id>/")
class CategoryDetailAPI(MethodView):
    @inject
    def __init__(
        self, category_service: CategoryServiceABC = Provide["category_service"]
    ):
        self.category_service = category_service

    @category_bp.response(200, CategorySchema())
    @category_bp.arguments(CategoryCreateSchema())
    def put(self, category_data, category_id):
        """ID 로 특정되는 카테고리 정보를 수정합니다."""
        try:
            return self.category_service.edit(
                category_id=category_id, category_data=category_data
            )
        except DataNotFound:
            abort(404)

    @category_bp.response(204)
    def delete(self, category_id: int):
        """ID 로 특정되는 카테고리를 하나 삭제합니다."""
        try:
            return self.category_service.delete(category_id)
        except DataNotFound:
            abort(404)


study_bp = Blueprint(
    name="StudyAPI",
    import_name=__name__,
    url_prefix="",
    description="스터디 관리를 위한 API 입니다.",
)


@study_bp.route("/studies/posts/")
class StudyListAPI(MethodView):
    def get(self):
        pass

    def post(self):
        pass
