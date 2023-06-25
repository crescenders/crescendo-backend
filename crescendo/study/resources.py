#########################
# Define your Blueprint.#
#########################
from flask.views import MethodView
from flask_smorest import Blueprint

from crescendo.study.schemas import CategoryListSchema

study_bp = Blueprint(
    name="StudyAPI",
    import_name=__name__,
    url_prefix="",
    description="스터디, 카테고리, 태그 관리를 위한 API 입니다.",
)


@study_bp.route("/categories/", tags=["CategoryAPI"])
class CategoryListAPI(MethodView):
    @study_bp.response(200, CategoryListSchema(many=True))
    def get(self):
        """카테고리 목록을 조회합니다."""
        pass

    @study_bp.response(201, CategoryListSchema())
    def post(self):
        """새로운 카테고리를 생성합니다."""
        pass


@study_bp.route("/categories/<int:category_id>", tags=["CategoryAPI"])
class CategoryDetailAPI(MethodView):
    def put(self):
        """ID 로 특정되는 카테고리 정보를 수정합니다."""
        pass

    def delete(self):
        """ID 로 특정되는 카테고리를 하나 삭제합니다."""
        pass


@study_bp.route("/studies/posts/", tags=["StudyAPI"])
class StudyListAPI(MethodView):
    def get(self):
        pass

    def post(self):
        pass
