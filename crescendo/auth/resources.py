from copy import deepcopy
from functools import wraps

from dependency_injector.wiring import Provide, inject
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from google.auth.transport import requests
from google.oauth2 import id_token

from crescendo.auth import auth_api
from crescendo.auth.containers import UserContainer
from crescendo.auth.schemas import UserListArgsSchema, UserListSchema, UserSchema


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

    @auth_api.arguments(UserListArgsSchema, location="query")
    @auth_api.response(200, UserListSchema)
    def get(self, kwargs):
        """사용자 목록을 조회합니다."""
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

    @auth_api.response(200, UserSchema)
    def get(self, user_uuid):
        """UUID 로 특정되는 사용자 한 명의 정보를 조회합니다."""
        return self.user_service.get_one_user(user_uuid)

    @auth_api.response(200, UserSchema)
    def put(self, user_uuid):
        """UUID로 특정되는 사용자 한 명의 정보를 수정합니다."""
        return self.user_service.update_user(user_uuid, **request.json)

    @auth_api.response(204)
    def delete(self, user_uuid):
        """UUID로 특정되는 사용자 한 명을 삭제합니다."""
        return self.user_service.withdraw(user_uuid)


def jwt_required_with_doc(*args, **kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            return jwt_required(*args, **kwargs)(func)(*f_args, **f_kwargs)

        wrapper._apidoc = deepcopy(getattr(func, "_apidoc", {}))
        wrapper._apidoc.setdefault("manual_doc", {})
        wrapper._apidoc["manual_doc"]["security"] = [{"Bearer Auth": []}]
        return wrapper

    return decorator


@auth_api.route("/login/google/", methods=["POST"])
@jwt_required_with_doc()
def google_login_api():
    """Google 소셜 로그인을 진행합니다."""
    # client_id = (
    #     "560831292125-jnlpjp0chs024i3p8hn7ifr7uidigqok.apps.googleusercontent.com"
    # )
    # token = token.get("jwt")
    # id_information = id_token.verify_oauth2_token(token, requests.Request(), client_id)
    # return {
    #     "Crescendo 서버에서 주는 ACCESS TOKEN": "이것은 Crescendo 서버에서 주는 Access Token!",
    #     "Crescendo 서버에서 주는 REFRESH TOKEN": "이것은 Crescendo 서버에서 주는 Refresh Token!",
    # }
