import random

import factory
from dateutil import relativedelta
from django.utils.datetime_safe import date
from factory.django import DjangoModelFactory
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.studygroup.models import Category, StudyGroup, StudyGroupMember

PAGINATION_LIST_FORMAT_KEYS = {
    "next",
    "previous",
    "results",
}
STUDYGROUP_FORMAT_KEYS = {
    "uuid",
    "head_image",
    "leaders",
    "post_title",
    "study_name",
    "until_deadline",
    "is_closed",
    "tags",
    "categories",
    "current_member_count",
    "member_limit",
}
LEADERS_FORMAT_KEYS = {
    "uuid",
    "username",
    "email",
}


class UserFactory(DjangoModelFactory):
    """
    유저를 생성합니다.
    """

    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class StudyGroupLeaderFactory(DjangoModelFactory):
    """
    스터디그룹장을 생성합니다.
    """

    class Meta:
        model = StudyGroupMember

    user = factory.SubFactory(UserFactory)
    is_approved = True
    is_leader = True
    request_message = factory.Faker("text")


class OpenedByDeadlineStudyGroupFactory(DjangoModelFactory):
    """
    오픈되어 있는 스터디그룹을 생성합니다.
    모집 마감이 오늘보다 이전인 경우의 스터디그룹들을 생성합니다.
    """

    class Meta:
        model = StudyGroup

    name = factory.Faker("name")
    member_limit = factory.LazyAttribute(lambda x: random.randrange(1, 10))
    content = factory.Faker("text")

    # deadline < today < start_date < end_date
    deadline = factory.Faker(
        "date_between_dates",
        date_start=date.today() + relativedelta.relativedelta(days=2),
        date_end=date.today() + relativedelta.relativedelta(days=10),
    )
    start_date = factory.LazyAttribute(
        lambda self: self.deadline
        + relativedelta.relativedelta(days=random.randrange(1, 20))
    )
    end_date = factory.LazyAttribute(
        lambda self: self.start_date
        + relativedelta.relativedelta(days=random.randrange(1, 30))
    )
    members = factory.RelatedFactory(StudyGroupLeaderFactory, "studygroup")


class StudyGroupListTestCase(APITestCase):
    """
    스터디그룹 목록 조회 API 테스트
    """

    @classmethod
    def setUpTestData(cls) -> None:
        # 카테고리 3개 생성
        categories = [Category(name=name) for name in ["백엔드", "프론트엔드", "데브옵스"]]
        Category.objects.bulk_create(categories)

        # 스터디그룹 10개 생성
        OpenedByDeadlineStudyGroupFactory.create_batch(10)

        for studygroup in StudyGroup.objects.all():
            print(studygroup.members.all())

    def test_read_list_format(self):
        url = reverse("studygroup_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # response.data 의 키들을 확인한다.
        self.assertEqual(set(response.data.keys()), PAGINATION_LIST_FORMAT_KEYS)
        # response.data["results"] 의 각 아이템들의 키들을 확인한다.
        for item in response.data["results"]:
            self.assertEqual(set(item.keys()), STUDYGROUP_FORMAT_KEYS)
            # response.data["results"] 의 각 아이템들의 "leaders" 의 각 아이템들의 키들을 확인한다.
            for leader in item["leaders"]:
                self.assertEqual(set(leader.keys()), LEADERS_FORMAT_KEYS)
