from dependency_injector import containers, providers
from fullask_rest_framework.factory.extensions import db

from crescendo.auth.repositories import UserRepositoryABC
from crescendo.study.repositories import (
    CategoryRepositoryABC,
    RecruitmentPostRepositoryABC,
    StudyGroupRepositoryABC,
)
from crescendo.study.services import CategoryServiceABC, StudyGroupServiceABC


class StudyContainer(containers.DeclarativeContainer):
    # 스터디그룹
    studygroup_service_abc = providers.Dependency(
        instance_of=StudyGroupServiceABC,
    )
    studygroup_repository_abc = providers.Dependency(
        instance_of=StudyGroupRepositoryABC,
    )
    recruitmentpost_repository_abc = providers.Dependency(
        instance_of=RecruitmentPostRepositoryABC,
    )
    studygroup_repository = providers.Singleton(
        studygroup_repository_abc,
        db=providers.Object(db),
    )
    recruitmentpost_repository = providers.Singleton(
        recruitmentpost_repository_abc,
        db=providers.Object(db),
    )
    user_repository_abc = providers.Dependency(
        instance_of=UserRepositoryABC  # type: ignore[type-abstract]
    )
    user_repository = providers.Singleton(  # UserRepository 에 필요한 종속성 주입
        user_repository_abc,
        db=providers.Object(db),
    )
    studygroup_service = providers.Singleton(
        studygroup_service_abc,
        studygroup_repository=studygroup_repository,
        recruitmentpost_repository=recruitmentpost_repository,
        user_repository=user_repository,
    )
    # 카테고리
    category_service_abc = providers.Dependency(
        instance_of=CategoryServiceABC  # type: ignore[type-abstract]
    )
    category_repository_abc = providers.Dependency(
        instance_of=CategoryRepositoryABC  # type: ignore[type-abstract]
    )
    category_repository = providers.Singleton(
        category_repository_abc,
        db=providers.Object(db),
    )
    category_service = providers.Singleton(
        category_service_abc,
        category_repository=category_repository,
    )
