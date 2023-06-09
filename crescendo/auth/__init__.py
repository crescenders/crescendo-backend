from dependency_injector import providers

from crescendo.auth.containers import UserContainer
from crescendo.auth.resources import AUTH_MICRO_APP
from crescendo.auth.services import UserService
from crescendo.study.repositories import SQLAlchemyFullCategoryRepository

BLUEPRINT = AUTH_MICRO_APP
MICROAPP_CONTAINER = UserContainer(
    user_service_abc=providers.Factory(UserService),
    user_repository_abc=providers.Factory(SQLAlchemyFullCategoryRepository),
)
