from dependency_injector import providers
from flask_smorest import Blueprint

from crescendo.users.containers import UserContainer
from crescendo.users.models import UserModel
from crescendo.users.services import UserService

users_api = Blueprint(
    "users",
    "users",
    description="사용자 API",
)


user_container = UserContainer()
user_container.user_service_factory.override(
    providers.Factory(UserService),  # type: ignore[type-abstract]
)
