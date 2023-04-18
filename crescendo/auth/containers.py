from dependency_injector import containers, providers

from core.entities.pagination import PaginationEntity
from crescendo.auth.entities import UserEntity
from crescendo.auth.models import UserModel
from crescendo.auth.repositories import UserRepositoryABC
from crescendo.auth.services import UserServiceABC


class UserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["crescendo.auth.resources"])

    # UserServiceABC 추상 클래스에 의존하도록 처리
    user_service_abc = providers.Dependency(
        instance_of=UserServiceABC  # type: ignore[type-abstract]
    )
    # UserRepositoryABC 추상 클래스에 의존하도록 처리
    user_repository_abc = providers.Dependency(
        instance_of=UserRepositoryABC  # type: ignore[type-abstract]
    )

    user_service = providers.Singleton(  # UserService 는 Singleton 으로 주입
        user_service_abc,
        user_repository=providers.Factory(  # UserRepository 에 필요한 종속성 주입
            user_repository_abc,
            user_model_cls=providers.Object(UserModel),
            pagination_entity_cls=providers.Object(PaginationEntity[UserEntity]),
            user_entity_cls=providers.Object(UserEntity),
        ),
        user_entity_cls=providers.Factory(UserEntity).provider,
    )
