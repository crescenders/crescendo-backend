from abc import ABC, abstractmethod

from fullask_rest_framework.db import make_transaction

from crescendo.auth.repositories import UserRepositoryABC
from crescendo.exceptions.service_exceptions import DataNotFound
from crescendo.study.models import CategoryModel, RecruitmentPostModel, StudyGroupModel
from crescendo.study.repositories import (
    CategoryRepositoryABC,
    RecruitmentPostRepositoryABC,
    StudyGroupRepositoryABC,
)


class CategoryServiceABC(ABC):
    @abstractmethod
    def create(self, category_category_data):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def edit(self, category_id, category_data):
        pass

    @abstractmethod
    def delete(self, category_id):
        pass


class CategoryService(CategoryServiceABC):
    def __init__(self, category_repository: CategoryRepositoryABC):
        self.category_repository = category_repository

    def create(self, category_data):
        new_category = self.category_repository.save(CategoryModel(**category_data))
        return new_category

    def get_all(self):
        return self.category_repository.read_all()

    def edit(self, category_id, category_data):
        category = self.category_repository.read_by_id(category_id)
        if category is None:
            raise DataNotFound
        category.name = category_data["name"]
        category.description = category_data["description"]
        return self.category_repository.save(category)

    def delete(self, category_id):
        category = self.category_repository.read_by_id(category_id)
        if category is None:
            raise DataNotFound
        return self.category_repository.delete(category)


class StudyGroupServiceABC(ABC):
    @abstractmethod
    def create_studygroup(self):
        """스터디그룹 홍보 게시물을 작성하고, 그에 맞는 정보로 새로운 스터디를 개설합니다."""
        pass

    @abstractmethod
    def get_post_list(self):
        pass

    @abstractmethod
    def get_study_list(self):
        pass

    @abstractmethod
    def edit(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class StudyGroupService(StudyGroupServiceABC):
    def __init__(
        self,
        studygroup_repository: StudyGroupRepositoryABC,
        recruitmentpost_repository: RecruitmentPostRepositoryABC,
        user_repository: UserRepositoryABC,
    ):
        self.studygroup_repository = studygroup_repository
        self.recruitmentpost_repository = recruitmentpost_repository
        self.user_repository = user_repository

    @make_transaction
    def create_studygroup(self, author_uuid, **studygroup_data):
        new_studygroup = StudyGroupModel(
            leader_id=self.user_repository.read_by_uuid(author_uuid).id,
            name=studygroup_data["name"],
            user_limit=studygroup_data["user_limit"],
            start_date=studygroup_data["start_date"],
            end_date=studygroup_data["end_date"],
        )
        self.studygroup_repository.save(new_studygroup)
        new_recruitmentpost = RecruitmentPostModel(
            studygroup_id=new_studygroup.id,
            title=studygroup_data["title"],
            content=studygroup_data["content"],
            deadline=studygroup_data["deadline"],
        )
        self.recruitmentpost_repository.save(new_recruitmentpost)
        return new_recruitmentpost

    def get_post_list(self):
        pass

    def get_study_list(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass
