from dependency_injector.wiring import Provide, inject
from flask import request
from flask.views import MethodView
from google.auth.exceptions import GoogleAuthError  # type: ignore[import]

from core.utils.jwt import jwt_required
from crescendo.auth import auth_api
from crescendo.auth.containers import UserContainer
from crescendo.auth.schemas import (GoogleOauthArgsSchema, UserListArgsSchema,
                                    UserListSchema, UserSchema)


@auth_api.route("/users/")
class UserListAPI(MethodView):
    """사용자 목록을 다루는 API 입니다."""

    @inject
    def __init__(
        self,
        *args,
        user_service=Provide[UserContainer.user_service],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.user_service = user_service

    @jwt_required()
    @auth_api.arguments(UserListArgsSchema, location="query")
    @auth_api.response(200, UserListSchema)
    def get(self, kwargs):
        """
        사용자 목록을 조회합니다.

        STAFF, ADMIN 권한을 가진 사람만 회원정보를 조회할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다
        """
        return self.user_service.get_list(**kwargs)


@auth_api.route("users/<uuid:user_uuid>/")
class UserDetailAPI(MethodView):
    """사용자 한 명을 다루는 API 입니다."""

    @inject
    def __init__(
        self,
        *args,
        user_service=Provide[UserContainer.user_service],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.user_service = user_service

    @jwt_required()
    @auth_api.response(200, UserSchema)
    def get(self, user_uuid):
        """UUID 로 특정되는 사용자 한 명의 정보를 조회합니다.

        본인, 혹은 STAFF, ADMIN 권한을 가진 사람만 회원정보를 조회할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다."""
        return self.user_service.get_one_user(user_uuid)

    @jwt_required()
    @auth_api.response(200, UserSchema)
    def put(self, user_uuid):
        """UUID로 특정되는 사용자 한 명의 정보를 수정합니다.

        본인, 혹은 STAFF, ADMIN 권한을 가진 사람만 회원정보를 수정할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다."""
        return self.user_service.update_user(user_uuid, **request.json)

    @jwt_required()
    @auth_api.response(204)
    @jwt_required()
    def delete(self, user_uuid):
        """UUID로 특정되는 사용자 한 명을 삭제합니다.

        본인, 혹은 STAFF, ADMIN 권한을 가진 사람만 회원탈퇴를 진행할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다."""
        return self.user_service.withdraw(user_uuid)


@auth_api.route("/login/google/", methods=["POST"])
@auth_api.arguments(GoogleOauthArgsSchema)
@inject
def google_login_api(
    google_oauth_token_data, user_service=Provide[UserContainer.user_service]
):
    """Google 소셜 로그인을 진행합니다.

    Google 에서 발급된 JWT 가 필요합니다.
    해당 JWT가 검증이 완료되면, 서버는 서비스 전용 JWT를 발급합니다.
    만약 새로운 사용자라면, 회원가입 또한 진행합니다."""

    google_oauth2_token = google_oauth_token_data.get("google_jwt")

    res = user_service.oauth2_login(oauth2_provider="google", data=google_oauth2_token)
    return res
