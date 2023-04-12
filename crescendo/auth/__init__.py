from dependency_injector import providers
from flask_smorest import Blueprint

from crescendo.auth.containers import UserContainer
from crescendo.auth.repositories import UserRepository
from crescendo.auth.services import UserService

auth_api = Blueprint(
    name="Auth API",
    import_name="auth_bp",
    description="로그인, 회원가입, 사용자 정보 조회를 위한 API 입니다.",
)

user_container = UserContainer(
    user_service_abc=providers.Factory(UserService),
    user_repository_abc=providers.Factory(UserRepository),
)
