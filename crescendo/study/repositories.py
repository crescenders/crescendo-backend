from abc import ABC

from fullask_rest_framework.repositories import SQLAlchemyFullRepository

from crescendo.study.models import CategoryModel, RecruitmentPostModel, StudyGroupModel


class CategoryRepositoryABC(SQLAlchemyFullRepository, ABC):
    pass


class CategoryRepository(CategoryRepositoryABC):
    def get_model(self):
        return CategoryModel


class StudyGroupRepositoryABC(SQLAlchemyFullRepository, ABC):
    pass


class StudyGroupRepository(StudyGroupRepositoryABC):
    def get_model(self):
        return StudyGroupModel


class RecruitmentPostRepositoryABC(SQLAlchemyFullRepository, ABC):
    pass


class RecruitmentPostRepository(RecruitmentPostRepositoryABC):
    def get_model(self):
        return RecruitmentPostModel
