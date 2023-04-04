from dependency_injector import providers
from flask_restx import Namespace

from crescendo.users.container import UserContainer
from crescendo.users.services import UserService

users_api = Namespace(
    "Users",
    description="사용자 리소스를 다루는 API입니다.",
)

user_container = UserContainer(user_service_abc=providers.Singleton(UserService))
