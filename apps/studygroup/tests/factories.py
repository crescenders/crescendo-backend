import random

import factory
from dateutil import relativedelta
from django.utils.datetime_safe import date
from factory.django import DjangoModelFactory

from apps.accounts.models import User
from apps.studygroup.models import Category, StudyGroup, StudyGroupMember


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category


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
    is_leader = True


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
