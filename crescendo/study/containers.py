from dependency_injector import containers, providers
from fullask_rest_framework.factory.extensions import db

from crescendo.study.repositories import SQLAlchemyFullCategoryRepositoryABC
from crescendo.study.services import CategoryServiceABC


class StudyContainer(containers.DeclarativeContainer):
    category_service_abc = providers.Dependency(
        instance_of=CategoryServiceABC  # type: ignore[type-abstract]
    )
    category_repository_abc = providers.Dependency(
        instance_of=SQLAlchemyFullCategoryRepositoryABC  # type: ignore[type-abstract]
    )
    category_repository = providers.Singleton(
        category_repository_abc,
        db=providers.Object(db),
    )
    category_service = providers.Singleton(
        category_service_abc,
        category_repository=category_repository,
    )
