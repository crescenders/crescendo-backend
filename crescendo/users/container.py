from dependency_injector import containers, providers

from crescendo.users.services import UserService, UserServiceABC


class UserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["crescendo.users.resources"]
    )
    user_service = providers.Factory(UserService)
