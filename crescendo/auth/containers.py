from dependency_injector import containers, providers

from crescendo.auth.repositories import UserRepositoryABC
from crescendo.auth.services import UserServiceABC


class UserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["crescendo.auth.resources"])

    user_service_abc = providers.Dependency(
        instance_of=UserServiceABC  # type: ignore[type-abstract]
    )
    user_repository_abc = providers.Dependency(
        instance_of=UserRepositoryABC  # type: ignore[type-abstract]
    )

    user_service = providers.Singleton(
        user_service_abc,
        user_repository=providers.Factory(user_repository_abc),
    )
