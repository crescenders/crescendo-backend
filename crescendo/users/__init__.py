from dependency_injector import providers
from flask_smorest import Blueprint

from crescendo.users.container import UserContainer
from crescendo.users.services import UserService

users_api = Blueprint(
    "users",
    "users",
    description="사용자 API",
)

user_container = UserContainer(user_service_abc=providers.Singleton(UserService))
