from dependency_injector.wiring import Provide, inject
from flask import request
from flask_restx import Resource

from crescendo.users import users_api
from crescendo.users.container import UserContainer
from crescendo.users.fields import user_list
from crescendo.users.services import UserService, UserServiceABC


@users_api.route("/")
class UserListAPI(Resource):
    @inject
    def __init__(
        self,
        *args,
        user_service=Provide[UserContainer.user_service_abc],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.user_service = user_service

    @users_api.marshal_with(user_list)
    @users_api.param("page", "페이지 번호", type=int, default=1)
    @users_api.param("per_page", "페이지당 게시물 수", type=int, default=10)
    @users_api.param("filter_by", "검색어", type=str)
    @users_api.param(
        "ordering", "정렬 조건", type=str, enum=["asc", "desc"], default="desc"
    )
    def get(self):
        """사용자 전체목록을 조회합니다.
        pagination 혹은 filter 결과가 있을 경우도 처리합니다."""

        page = int(request.args.get("page")) if request.args.get("page") else 1
        per_page = (
            int(request.args.get("per_page")) if request.args.get("per_page") else 10
        )
        filter_by = (
            str(request.args.get("filter_by"))
            if request.args.get("filter_by")
            else None
        )
        ordering = (
            str(request.args.get("ordering"))
            if request.args.get("ordering")
            else "desc"
        )

        return self.user_service.get_lists(
            page=page, per_page=per_page, filter_by=filter_by, ordering=ordering
        )

    def post(self):
        """사용자 한 명을 생성합니다.
        비밀번호를 암호화하여 저장합니다."""
        return self.user_service.register()


@users_api.route("/<uuid:user_uuid>/")
class UserDetail(Resource):
    @inject
    def __init__(
        self,
        *args,
        user_service=Provide[UserContainer.user_service_abc],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.user_service = user_service

    def get(self, user_uuid):
        """UUID 로 특정되는 사용자 한 명의 정보를 조회합니다."""
        return self.user_service.get_one_user(user_uuid)

    # def put(self, user_uuid):
    #     """UUID로 특정되는 사용자 한 명의 정보를 수정합니다."""
    #     return self.user_service.update_user(user_uuid, **request.json)

    def delete(self, user_uuid):
        """UUID로 특정되는 사용자 한 명을 삭제합니다."""
        return self.user_service.withdraw(user_uuid)
