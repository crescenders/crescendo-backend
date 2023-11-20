from datetime import timedelta

from django.core.files.storage import default_storage
from django.utils.datetime_safe import date
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.studygroup.models import Category, StudyGroup, StudyGroupMember, Tag
from apps.studygroup.tests.utils import create_dummy_image

DETAIL_FORMAT_KEYS = {
    "uuid",
    "head_image",
    "leaders",
    "post_title",
    "post_content",
    "created_at",
    "updated_at",
    "study_name",
    "start_date",
    "end_date",
    "deadline",
    "until_deadline",
    "is_closed",
    "tags",
    "categories",
    "current_member_count",
    "member_limit",
}

LEADER_FORMAT_KEYS = {
    "uuid",
    "username",
    "email",
}


class BaseStudyGroupTestCase(APITestCase):
    def setUp(self):
        # 태그 생성
        tags = [Tag(name=name) for name in ["Python", "Django", "React"]]
        Tag.objects.bulk_create(tags)

        # 카테고리 생성
        categories = [Category(name=name) for name in ["백엔드", "프론트엔드", "데브옵스"]]
        Category.objects.bulk_create(categories)

        # 유저 생성
        self.django_study_leader = User.objects.create_user(
            username="django_study_leader",
            password="password",
            email="django@django.com",
        )
        self.another_user = User.objects.create_user(
            username="another_user",
            password="password",
            email="another@another.com",
        )

        # 스터디그룹 생성
        self.django_study = StudyGroup.objects.create(
            name="Django 스터디",
            member_limit=2,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            deadline=date.today() - timedelta(days=1),
            title="Django 스터디 모집합니다.",
            content="Django 는 파이썬 기반의 오픈소스 웹 프레임워크입니다. Django 를 함께 공부하실 분들을 모집합니다.",
        )
        self.django_study.members.add(
            StudyGroupMember.objects.create(
                user=self.django_study_leader,
                studygroup=self.django_study,
                is_leader=True,
            ),
        )

        self.react_study = StudyGroup.objects.create(
            head_image=create_dummy_image("react.png"),
            name="React 스터디",
            member_limit=2,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            deadline=date.today() - timedelta(days=1),
            title="React 스터디 모집합니다.",
            content="React 는 페이스북에서 만든 프론트엔드 라이브러리입니다. React 를 함께 공부하실 분들을 모집합니다.",
        )
        self.react_study.members.add(
            StudyGroupMember.objects.create(
                user=self.django_study_leader,
                studygroup=self.react_study,
                is_leader=True,
            ),
        )

    def tearDown(self) -> None:
        default_storage.delete(self.react_study.head_image.name)

    def test_read_detail_format_without_head_image(self):
        url = reverse(
            "studygroup-detail", kwargs={"studygroup_uuid": self.django_study.uuid}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"response: {response.data}")
        # response.data 의 키들을 확인한다.
        self.assertEqual(
            set(response.data.keys()), DETAIL_FORMAT_KEYS, f"response: {response.data}"
        )
        # head_image 가 없는 경우, 랜덤 이미지 주소인 picsum.photos 로 대체된다.
        self.assertTrue(
            response.data["head_image"].startswith("https://picsum.photos"),
            f"response: {response.data}",
        )
        # 리더 정보에는 유저의 uuid, username 만 포함되어야 한다.
        self.assertEqual(
            set(response.data["leaders"][0].keys()),
            LEADER_FORMAT_KEYS,
            f"response: {response.data}",
        )

    def test_read_detail_format_with_head_image(self):
        url = reverse(
            "studygroup-detail", kwargs={"studygroup_uuid": self.react_study.uuid}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"response: {response.data}")
        # response.data 의 키들을 확인한다.
        self.assertEqual(
            set(response.data.keys()), DETAIL_FORMAT_KEYS, f"response: {response.data}"
        )
        # head_image 가 있으므로, 해당 이미지의 주소가 그대로 들어간다.
        self.assertTrue(
            response.data["head_image"].split("/")[-1],
            self.react_study.head_image.name,
        )
        # 리더 정보에는 유저의 uuid, username 만 포함되어야 한다.
        self.assertEqual(
            set(response.data["leaders"][0].keys()),
            LEADER_FORMAT_KEYS,
            f"response: {response.data}",
        )
