#########################
# Define your Blueprint.#
#########################
from dependency_injector.wiring import Provide, inject
from flask.views import MethodView
from flask_smorest import Blueprint

from crescendo.study.schemas import CategoryListSchema
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

    @category_bp.response(200, CategoryListSchema(many=True))
    def get(self):
        """카테고리 목록을 조회합니다."""
        return self.category_service.get_all()

    @category_bp.response(201, CategoryListSchema())
    def post(self):
        """새로운 카테고리를 생성합니다."""
        return self.category_service.create()


@category_bp.route("/categories/<int:category_id>/")
class CategoryDetailAPI(MethodView):
    @inject
    def __init__(
        self, category_service: CategoryServiceABC = Provide["category_service"]
    ):
        self.category_service = category_service

    @category_bp.response(200, CategoryListSchema(many=True))
    def put(self):
        """ID 로 특정되는 카테고리 정보를 수정합니다."""
        return self.category_service.edit()

    @category_bp.response(204, CategoryListSchema(many=True))
    def delete(self):
        """ID 로 특정되는 카테고리를 하나 삭제합니다."""
        return self.category_service.delete()


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
