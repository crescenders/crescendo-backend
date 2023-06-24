from dependency_injector import providers

from crescendo.auth.containers import UserContainer
from crescendo.auth.repositories import FullUserRepository
from crescendo.auth.resources import auth_bp
from crescendo.auth.services import UserService

BLUEPRINT = auth_bp
MICROAPP_CONTAINER = UserContainer(
    user_service_abc=providers.Factory(UserService),
    user_repository_abc=providers.Factory(FullUserRepository),
)
