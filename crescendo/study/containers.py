from dependency_injector import containers, providers
from fullask_rest_framework.factory.extensions import db

from crescendo.study.entities import CategoryEntity
from crescendo.study.models import CategoryModel
from crescendo.study.repositories import SQLAlchemyFullCategoryRepositoryABC
from crescendo.study.services import CategoryServiceABC


class StudyContainer(containers.DeclarativeContainer):
    category_service_abc = providers.Dependency(
        instance_of=CategoryServiceABC
    )  # type: ignore[type-abstract]

    category_repository_abc = providers.Dependency(
        instance_of=SQLAlchemyFullCategoryRepositoryABC
    )  # type: ignore[type-abstract]

    category_repository = providers.Singleton(
        category_repository_abc,
        db=providers.Object(db),
        entity=providers.Object(CategoryEntity),
        sqlalchemy_model=providers.Object(CategoryModel),
    )
    user_service = providers.Singleton(
        category_service_abc,
        user_repository=category_repository,
        user_entity=providers.Factory(CategoryEntity).provider,
    )
