from abc import ABC, abstractmethod

from fullask_rest_framework.db import make_transaction
from fullask_rest_framework.httptypes import PaginationResponse

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

    @make_transaction
    def create(self, category_data):
        new_category = self.category_repository.save(CategoryModel(**category_data))
        return new_category

    def get_all(self):
        return self.category_repository.read_all()

    @make_transaction
    def edit(self, category_id, category_data):
        category = self.category_repository.read_by_id(category_id)
        if category is None:
            raise DataNotFound
        category.name = category_data["name"]
        category.description = category_data["description"]
        return self.category_repository.save(category)

    @make_transaction
    def delete(self, category_id):
        category = self.category_repository.read_by_id(category_id)
        if category is None:
            raise DataNotFound
        return self.category_repository.delete(category)


class StudyGroupServiceABC(ABC):
    @abstractmethod
    def create_studygroup(self, author_uuid, **studygroup_data):
        """스터디그룹 홍보 게시물을 작성하고, 그에 맞는 정보로 새로운 스터디를 개설합니다."""
        pass

    @abstractmethod
    def get_post_list(
        self,
        pagination_request,
        sorting_request,
    ) -> PaginationResponse:
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
        category_repository: CategoryRepositoryABC,
    ):
        self.studygroup_repository = studygroup_repository
        self.recruitmentpost_repository = recruitmentpost_repository
        self.user_repository = user_repository
        self.category_repository = category_repository

    @make_transaction
    def create_studygroup(self, author_uuid, **studygroup_data):
        categories = self.category_repository.read_all_by_ids(
            studygroup_data["category_ids"]
        )
        # TODO: 에러 처리하기
        if None in categories:
            raise Exception("카테고리가 존재하지 않습니다.")
        new_studygroup = StudyGroupModel(
            leader_id=self.user_repository.read_by_uuid(author_uuid).id,
            category_set=categories,
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

    def get_post_list(
        self,
        pagination_request,
        sorting_request,
    ) -> PaginationResponse:
        return self.recruitmentpost_repository.read_all(
            pagination_request=pagination_request,
            sorting_request=sorting_request,
        )

    def get_study_list(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass
