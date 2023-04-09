from dependency_injector.wiring import Provide, inject
from flask import request
from flask.views import MethodView

from crescendo.users import users_api
from crescendo.users.containers import UserContainer
from crescendo.users.schemas import UserListArgsSchema, UserListSchema


@users_api.route("/")
class UserListAPI(MethodView):
    @inject
    def __init__(
        self,
        *args,
        user_service=Provide[UserContainer.user_service],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.user_service = user_service

    @users_api.arguments(UserListArgsSchema, location="query")
    @users_api.response(200, UserListSchema)
    def get(self, kwargs):
        """사용자 목록을 조회합니다."""
        return self.user_service.get_list(**kwargs)

    def post(self):
        """사용자 한 명을 생성합니다."""
        return self.user_service.register()


@users_api.route("/<uuid:user_uuid>/")
class UserDetail(MethodView):
    @inject
    def __init__(
        self,
        *args,
        user_service=Provide[UserContainer.user_service],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.user_service = user_service

    def get(self, user_uuid):
        """UUID 로 특정되는 사용자 한 명의 정보를 조회합니다."""
        return self.user_service.get_one_user(user_uuid)

    def put(self, user_uuid):
        """UUID로 특정되는 사용자 한 명의 정보를 수정합니다."""
        return self.user_service.update_user(user_uuid, **request.json)

    def delete(self, user_uuid):
        """UUID로 특정되는 사용자 한 명을 삭제합니다."""
        return self.user_service.withdraw(user_uuid)
