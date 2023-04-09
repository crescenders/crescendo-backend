from dependency_injector import providers
from flask_smorest import Blueprint

from crescendo.users.containers import UserContainer
from crescendo.users.models import UserModel
from crescendo.users.repositories import UserRepository, UserRepositoryABC
from crescendo.users.services import UserService

users_api = Blueprint(
    "users",
    "users",
    description="사용자 API",
)


user_container = UserContainer(
    user_service_abc=providers.Factory(UserService),
    user_repository_abc=providers.Factory(UserRepository),
)
