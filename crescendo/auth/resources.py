from uuid import UUID

from dependency_injector.wiring import Provide, inject
from flask.views import MethodView
from flask_jwt_extended import get_jwt
from flask_smorest import Blueprint, abort
from fullask_rest_framework.schemas.pagination import PaginationRequestSchema
from fullask_rest_framework.schemas.sorting import SortingRequestSchema
from fullask_rest_framework.utils.jwt import jwt_required
from fullask_rest_framework.vo.filtering import FilteringRequest
from fullask_rest_framework.vo.pagination import PaginationRequest
from fullask_rest_framework.vo.sorting import SortingRequest
from google.auth.exceptions import GoogleAuthError  # type: ignore[import]

from crescendo.auth.schemas import (
    GoogleOauthArgsSchema,
    JWTSchema,
    PaginatedUserListSchema,
    UserFilteringArgsSchema,
    UserSchema,
)
from crescendo.auth.services import UserServiceABC
from crescendo.exceptions.service_exceptions import DataNotFound

#########################
# Define your Blueprint.#
#########################

AUTH_MICRO_APP = Blueprint(
    name="AuthAPI",
    import_name=__name__,
    url_prefix="/auth",
    description="로그인, 회원가입, 사용자 정보 조회 및 수정을 위한 API 입니다.",
)


#############################
# Define your API endpoints.#
#############################


@AUTH_MICRO_APP.route("/users/")
class UserListAPI(MethodView):
    """사용자 목록을 다루는 API 입니다."""

    @inject
    def __init__(self, user_service: UserServiceABC = Provide["user_service"]):
        self.user_service = user_service

    # @jwt_required()
    @AUTH_MICRO_APP.arguments(PaginationRequestSchema, location="query")  # 페이지네이션 파라미터
    @AUTH_MICRO_APP.arguments(SortingRequestSchema, location="query")  # 정렬 파라미터
    @AUTH_MICRO_APP.arguments(UserFilteringArgsSchema, location="query")  # 필터링 파라미터
    @AUTH_MICRO_APP.response(200, PaginatedUserListSchema)
    def get(
        self,
        pagination_request: PaginationRequest,
        sorting_request: SortingRequest,
        filtering_request: FilteringRequest,
    ):
        """사용자 목록을 조회합니다."""
        return self.user_service.get_list(
            pagination_request=pagination_request,
            sorting_request=sorting_request,
            filtering_request=filtering_request,
        )


@AUTH_MICRO_APP.route("users/<uuid:user_uuid>/")
class UserDetailAPI(MethodView):
    """사용자 한 명을 다루는 API 입니다."""

    @inject
    def __init__(self, user_service: UserServiceABC = Provide["user_service"]):
        self.user_service = user_service

    # @jwt_required()
    @AUTH_MICRO_APP.response(200, UserSchema)
    @AUTH_MICRO_APP.alt_response(404, description="UUID 로 사용자를 특정할 수 없을 때 발생합니다.")
    def get(self, user_uuid: UUID):
        """
        UUID 로 특정되는 사용자 한 명의 정보를 조회합니다.

        데이터베이스에 없는 UUID 로 사용자를 조회하고자 시도한다면, 404 NOT FOUND 를 응답합니다. <br/>
        (권한 부분 구현 X)<br/>
        본인, 혹은 STAFF, ADMIN 권한을 가진 사람만 회원정보를 조회할 수 있습니다.<br/>
        Crescendo 서비스에서 발급된 JWT가 필요합니다.<br/>
        """
        try:
            return self.user_service.get_one(str(user_uuid))
        except DataNotFound:
            abort(404)

    # @jwt_required()

    @AUTH_MICRO_APP.arguments(UserSchema)
    @AUTH_MICRO_APP.response(200, UserSchema)
    @AUTH_MICRO_APP.alt_response(404, description="UUID 로 사용자를 특정할 수 없을 때 발생합니다.")
    def put(self, data, user_uuid: UUID):
        """
        UUID로 특정되는 사용자 한 명의 정보를 수정합니다.

        닉네임만 수정할 수 있습니다.
        본인, 혹은 STAFF, ADMIN 권한을 가진 사람만 회원정보를 수정할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다.
        """
        if not data:
            abort(400)
        try:
            return self.user_service.edit_info(user_uuid=str(user_uuid), data=data)
        except DataNotFound:
            abort(404)

    # @jwt_required()
    @AUTH_MICRO_APP.response(204)
    @AUTH_MICRO_APP.alt_response(404, description="UUID 로 사용자를 특정할 수 없을 때 발생합니다.")
    def delete(self, user_uuid: UUID):
        """
        UUID로 특정되는 사용자 한 명을 삭제합니다.

        본인, 혹은 STAFF, ADMIN 권한을 가진 사람만 회원탈퇴를 진행할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다.
        """
        try:
            return self.user_service.withdraw(user_uuid=str(user_uuid))
        except DataNotFound:
            abort(404)


@AUTH_MICRO_APP.post("/login/google/")
@AUTH_MICRO_APP.arguments(GoogleOauthArgsSchema)
@AUTH_MICRO_APP.response(200, JWTSchema)
@inject
def google_login_api(
    google_oauth_token, user_service: UserServiceABC = Provide["user_service"]
):
    """
    Google 소셜 로그인을 진행합니다.

    Google 에서 발급된 JWT 가 필요합니다.
    해당 JWT가 검증이 완료되면, 서버는 서비스 전용 JWT를 발급합니다.
    만약 새로운 사용자라면, 회원가입 또한 진행합니다.
    """
    return user_service.google_login(data=google_oauth_token["google_jwt"])


@AUTH_MICRO_APP.post("/login/refresh/")
@AUTH_MICRO_APP.response(200, JWTSchema)
@inject
@jwt_required(refresh=True)
def refresh_token_api(user_service: UserServiceABC = Provide["user_service"]):
    """refresh token 으로 토큰을 재발급받습니다."""

    return user_service.refresh_login(decoded_refresh_token=get_jwt())
