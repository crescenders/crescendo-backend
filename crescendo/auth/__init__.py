from dependency_injector import providers
from fullask_rest_framework.factory.microapp import MicroApp

from crescendo.auth.containers import UserContainer
from crescendo.auth.repositories import RoleRepository, UserRepository
from crescendo.auth.resources import auth_bp
from crescendo.auth.services import UserService


class AuthMicroApp(MicroApp):
    blueprints = (auth_bp,)
    microapp_container = UserContainer(
        user_service_abc=providers.Singleton(UserService),
        user_repository_abc=providers.Singleton(UserRepository),
        role_repository_abc=providers.Singleton(RoleRepository),
    )
