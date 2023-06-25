from dependency_injector import providers

from crescendo.study.containers import StudyContainer
from crescendo.study.repositories import SQLAlchemyFullCategoryRepository
from crescendo.study.resources import study_bp
from crescendo.study.services import CategoryService

BLUEPRINT = study_bp
MICROAPP_CONTAINER = StudyContainer(
    category_service_abc=providers.Factory(CategoryService),
    category_repository_abc=providers.Factory(SQLAlchemyFullCategoryRepository),
)
