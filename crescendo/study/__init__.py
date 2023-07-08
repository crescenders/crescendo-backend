from dependency_injector import providers
from fullask_rest_framework.factory.microapp import MicroApp

from crescendo.study.containers import StudyContainer
from crescendo.study.repositories import (
    CategoryRepository,
    RecruitmentPostRepository,
    StudyGroupRepository,
)
from crescendo.study.resources import category_bp, study_bp
from crescendo.study.services import CategoryService, StudyGroupService


class StudyMicroApp(MicroApp):
    blueprints = (study_bp, category_bp)
    microapp_container = StudyContainer(
        studygroup_service_abc=providers.Singleton(StudyGroupService),
        studygroup_repository_abc=providers.Singleton(StudyGroupRepository),
        recruitmentpost_repository_abc=providers.Singleton(RecruitmentPostRepository),
        category_service_abc=providers.Singleton(CategoryService),
        category_repository_abc=providers.Singleton(CategoryRepository),
    )
