#########################
# Define your Blueprint.#
#########################
from dependency_injector.wiring import Provide, inject
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint, abort
from fullask_rest_framework.utils import jwt_required

from crescendo.exceptions.service_exceptions import DataNotFound
from crescendo.study.schemas import (
    CategoryCreateSchema,
    CategorySchema,
    RecruitmentPostReadSchema,
    StudyGroupCreateSchema,
)
from crescendo.study.services import CategoryServiceABC, StudyGroupServiceABC

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
    @inject
    def __init__(
        self, studygroup_service: StudyGroupServiceABC = Provide["studygroup_service"]
    ):
        self.studygroup_service = studygroup_service

    def get(self):
        """스터디그룹 홍보 게시물들을 조회합니다."""
        return self.studygroup_service.get_study_list()

    @jwt_required()
    @study_bp.arguments(StudyGroupCreateSchema)
    @study_bp.response(201, RecruitmentPostReadSchema)
    def post(self, studygroup_data):
        """스터디그룹을 개설하고, 스터디그룹 홍보 게시물을 생성합니다."""
        author_uuid = get_jwt_identity()
        return self.studygroup_service.create_studygroup(
            **studygroup_data, author_uuid=author_uuid
        )
