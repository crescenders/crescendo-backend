from dependency_injector import containers, providers
from fullask_rest_framework.factory.extensions import db

from crescendo.auth.repositories import UserRepositoryABC
from crescendo.auth.services import UserServiceABC


class UserContainer(containers.DeclarativeContainer):
    # UserServiceABC 추상 클래스에 의존하도록 처리
    user_service_abc = providers.Dependency(
        instance_of=UserServiceABC  # type: ignore[type-abstract]
    )
    # CRUDRepositoryABC 추상 클래스에 의존하도록 처리
    user_repository_abc = providers.Dependency(
        instance_of=UserRepositoryABC  # type: ignore[type-abstract]
    )
    user_repository = providers.Singleton(  # UserRepository 에 필요한 종속성 주입
        user_repository_abc,
        db=providers.Object(db),
    )
    user_service = providers.Singleton(  # UserService 는 Singleton 으로 주입
        user_service_abc,
        user_repository=user_repository,
    )
