from dependency_injector.wiring import Provide, inject
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from google.auth.exceptions import GoogleAuthError  # type: ignore[import]

from core.schemas.pagination import PaginationArgsSchema
from core.utils.jwt import jwt_required
from crescendo.auth.schemas import (GoogleOauthArgsSchema,
                                    PaginatedUserListSchema, SortingArgsSchema,
                                    UserFilteringArgsSchema, UserSchema)

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
    @AUTH_MICRO_APP.arguments(PaginationArgsSchema, location="query")  # 페이지네이션 파라미터
    @AUTH_MICRO_APP.arguments(SortingArgsSchema, location="query")  # 정렬 파라미터
    @AUTH_MICRO_APP.arguments(UserFilteringArgsSchema, location="query")  # 필터링 파라미터
    @AUTH_MICRO_APP.response(200, PaginatedUserListSchema)
    def get(
        self,
        paginate_args,
        sorting_args,
        filtering_args,
    ):
        """
        사용자 목록을 조회합니다.

        - `권한`: STAFF, ADMIN 권한을 가진 사람만 회원정보를 조회할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다.

        - `페이지네이션`: `per_page` 로 한 페이지에 나타내고자 하는 아이템의 개수를,
        `page` 로 조회하고자 하는 페이지 번호를 전달할 수 있습니다.
        아무런 값도 전달되지 않을 경우, 기본적으로 `per_page` 에는 10이, `page` 에는 1이 할당됩니다.

        - `필터링`: 기본적으로 OR 조건이 적용됩니다.
        예컨대, `/users/?username=hi&email=goddessana` 는
        "username 에 'hi' 가 포함되고, email에 'goddessana' 가 포함된 모든 사용자" 를 응답합니다.

        - `정렬`: `?sorting` 을 통해서 어떻게 정렬하고자 하는지를 전달할 수 있습니다.
        예컨대, `/users/?sorting=username:desc,email:asc` 는
        "username 에 대해서 오름차순으로 정렬하고, email에 대해서 내림차순으로 정렬한 사용자의 모든 목록" 을 응답합니다.

        """
        # {'page': 1, 'per_page': 12}
        # {'sorting': [{'id': 'asc'}]}
        # {'email': 'hi', 'username': 'hello'}
        return self.user_service.get_list(paginate_args, sorting_args, filtering_args)


@AUTH_MICRO_APP.route("users/<uuid:user_uuid>/")
class UserDetailAPI(MethodView):
    """사용자 한 명을 다루는 API 입니다."""

    @inject
    def __init__(self, user_service=Provide["user_service"]):
        self.user_service = user_service

    # @jwt_required()
    @AUTH_MICRO_APP.response(200, UserSchema)
    def get(self, user_uuid):
        """UUID 로 특정되는 사용자 한 명의 정보를 조회합니다.

        본인, 혹은 STAFF, ADMIN 권한을 가진 사람만 회원정보를 조회할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다."""
        return self.user_service.get_one(user_uuid)

    @jwt_required()
    @AUTH_MICRO_APP.response(200, UserSchema)
    def put(self, user_uuid):
        """UUID로 특정되는 사용자 한 명의 정보를 수정합니다.

        본인, 혹은 STAFF, ADMIN 권한을 가진 사람만 회원정보를 수정할 수 있습니다.
        Crescendo 서비스에서 발급된 JWT가 필요합니다."""
        return self.user_service.update_user(user_uuid, **request.json)

    @jwt_required()
    @AUTH_MICRO_APP.response(204)
    @jwt_required()
    def delete(self, user_uuid):
        """UUID로 특정되는 사용자 한 명을 삭제합니다.

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
