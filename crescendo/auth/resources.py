from dependency_injector.wiring import Provide, inject
from flask.views import MethodView
from flask_smorest import Blueprint
from google.auth.exceptions import GoogleAuthError  # type: ignore[import]

from core.entities.pagination import PaginationRequest
from core.schemas.pagination import PaginationRequestSchema
from core.schemas.sorting import SortingRequestSchema
from core.utils.jwt import jwt_required
from crescendo.auth.schemas import (
    GoogleOauthArgsSchema,
    PaginatedUserListSchema,
    UserFilteringArgsSchema,
    UserSchema,
)

#########################
# Define your Blueprint.#
#########################

AUTH_MICRO_APP = Blueprint(
    name="AuthAPI",
    import_name=__name__,
    url_prefix="/auth",
    description="로그인, 회원가입, 사용자 정보 조회를 위한 API 입니다.",
)


#############################
# Define your API endpoints.#
#############################


@AUTH_MICRO_APP.route("/users/")
class UserListAPI(MethodView):
    """사용자 목록을 다루는 API 입니다."""

    @inject
    def __init__(self, user_service=Provide["user_service"]):
        self.user_service = user_service

    # @jwt_required()
    @AUTH_MICRO_APP.arguments(PaginationRequestSchema, location="query")  # 페이지네이션 파라미터
    @AUTH_MICRO_APP.arguments(SortingRequestSchema, location="query")  # 정렬 파라미터
    @AUTH_MICRO_APP.arguments(UserFilteringArgsSchema, location="query")  # 필터링 파라미터
    @AUTH_MICRO_APP.response(200, PaginatedUserListSchema)
    def get(
        self,
        pagination_request: PaginationRequest,
        sorting_request,
        filtering_request,
    ):
        """
        사용자 목록을 조회합니다.
        """
        # print(sorting_request)
        # print(pagination_request)
        # print(filtering_request)
        return self.user_service.get_list(
            pagination_request=pagination_request,
            sorting_request=sorting_request,
            filtering_request=filtering_request,
        )


@AUTH_MICRO_APP.route("users/<string:user_uuid>/")
class UserDetailAPI(MethodView):
    """사용자 한 명을 다루는 API 입니다."""

    @inject
    def __init__(self, user_service=Provide["user_service"]):
        self.user_service = user_service

    # @jwt_required()
    @AUTH_MICRO_APP.response(200, UserSchema)
    def get(self, user_uuid):
        """ID 로 특정되는 사용자 한 명의 정보를 조회합니다.

        본인, 혹은 STAFF, ADMIN 권한을 가진 사람만 회원정보를 조회할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다."""
        return self.user_service.get_one(user_uuid)

    # @jwt_required()

    @AUTH_MICRO_APP.arguments(UserSchema)
    @AUTH_MICRO_APP.response(200, UserSchema)
    def put(self, data, user_uuid):
        """ID로 특정되는 사용자 한 명의 정보를 수정합니다.

        닉네임만 수정할 수 있습니다.
        본인, 혹은 STAFF, ADMIN 권한을 가진 사람만 회원정보를 수정할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다.
        """

        return self.user_service.edit_info(user_uuid=user_uuid, data=data)

    # @jwt_required()
    @AUTH_MICRO_APP.response(204)
    def delete(self, user_uuid):
        """ID로 특정되는 사용자 한 명을 삭제합니다.

        본인, 혹은 STAFF, ADMIN 권한을 가진 사람만 회원탈퇴를 진행할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다."""
        return self.user_service.withdraw(user_uuid)


@AUTH_MICRO_APP.post("/login/google/")
@AUTH_MICRO_APP.arguments(GoogleOauthArgsSchema)
@inject
def google_login_api(google_oauth_token_data, user_service=Provide["user_service"]):
    """Google 소셜 로그인을 진행합니다.

    Google 에서 발급된 JWT 가 필요합니다.
    해당 JWT가 검증이 완료되면, 서버는 서비스 전용 JWT를 발급합니다.
    만약 새로운 사용자라면, 회원가입 또한 진행합니다."""

    google_oauth2_token = google_oauth_token_data.get("google_jwt")

    res = user_service.oauth2_login(oauth2_provider="google", data=google_oauth2_token)
    return res
