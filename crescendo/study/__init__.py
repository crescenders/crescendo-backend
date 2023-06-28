from dependency_injector import providers
from fullask_rest_framework.factory.microapp import MicroApp

from crescendo.study.containers import StudyContainer
from crescendo.study.repositories import SQLAlchemyFullCategoryRepository
from crescendo.study.resources import category_bp, study_bp
from crescendo.study.services import CategoryService


class StudyMicroApp(MicroApp):
    blueprints = (study_bp, category_bp)
    microapp_container = StudyContainer(
        category_service_abc=providers.Factory(CategoryService),
        category_repository_abc=providers.Factory(SQLAlchemyFullCategoryRepository),
    )
