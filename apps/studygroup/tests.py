from datetime import timedelta

from django.utils.datetime_safe import date
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.studygroup.models import Category, StudyGroup, StudyGroupMember, Tag


class BaseStudyGroupTestCase(APITestCase):
    def setUp(self):
        # 태그 생성
        tag_names = [
            "웹 개발",
            "데이터 분석",
            "알고리즘",
            "클라우드",
            "보안",
            "인공지능",
            "머신러닝",
        ]
        tags = [Tag(name=name) for name in tag_names]
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
                study_group=self.django_study,
                is_leader=True,
            ),
        )

        self.python_study = StudyGroup.objects.create(
            name="Python 스터디",
            member_limit=2,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            deadline=date.today() - timedelta(days=1),
            title="Python 스터디 모집합니다.",
            content=(
                "Python 은 인터프리터 언어로, 배우기 쉽고 강력한 프로그래밍 언어입니다."
                " Python 을 함께 공부하실 분들을 모집합니다."
            ),
        )
        self.python_study.members.add(
            StudyGroupMember.objects.create(
                user=self.django_study_leader,
                study_group=self.python_study,
                is_leader=True,
            ),
        )

        self.react_study = StudyGroup.objects.create(
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
                study_group=self.react_study,
                is_leader=True,
            ),
        )


class CategoryTestCase(BaseStudyGroupTestCase):
    """
    카테고리 API 테스트
    """

    def test_read_categories(self):
        url = reverse("category_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(
            response.data,
            [{"name": "백엔드"}, {"name": "프론트엔드"}, {"name": "데브옵스"}],
        )


class StudyGroupDeleteTestCase(BaseStudyGroupTestCase):
    def test_delete_studygroup_only_leader(self):
        """
        스터디그룹 삭제는 스터디그룹장만 가능합니다.
        """
        # 로그인
        self.client.force_login(self.django_study_leader)

        # 스터디그룹 삭제 전
        self.assertEqual(StudyGroup.objects.count(), 3)

        # 스터디그룹 삭제
        url = reverse(
            "studygroup_detail", kwargs={"uuid": StudyGroup.objects.first().uuid}
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(StudyGroup.objects.count(), 2)

    def test_delete_studygroup_not_leader(self):
        """
        다른 스터디원은 스터디그룹을 삭제할 수 없습니다.
        """
        # 로그인
        self.client.force_login(self.another_user)

        # 스터디그룹 삭제 전
        self.assertEqual(StudyGroup.objects.count(), 3)

        # 스터디그룹 삭제
        url = reverse(
            "studygroup_detail", kwargs={"uuid": StudyGroup.objects.first().uuid}
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(StudyGroup.objects.count(), 3)


class StudyGroupReadTestCase(BaseStudyGroupTestCase):
    def test_read_studygroup_auth(self):
        """
        스터디그룹 목록 조회는 아무런 인증 정보 없이 할 수 있어야 합니다.
        """
        url = reverse("studygroup_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
