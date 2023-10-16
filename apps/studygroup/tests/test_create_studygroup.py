from datetime import timedelta

from django.utils.datetime_safe import date
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.models import StudyGroup
from apps.studygroup.tests.factories import CategoryFactory, UserFactory


class CreateStudyGroupTestCase(APITestCase):
    def setUp(self) -> None:
        CategoryFactory(name="Django")
        self.logged_in_user = UserFactory()

    def tearDown(self):
        for studygroup in StudyGroup.objects.all():
            studygroup.head_image.delete()

    def test_not_logged_in_user_cannot_create_studygroup(self):
        """
        스터디그룹 생성은 로그인하지 않으면 불가능합니다.
        """
        url = reverse("studygroup_list")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401, f"response: {response.data}")

    def test_logged_in_user_can_create_studygroup(self):
        """
        스터디그룹 생성은 로그인한 유저만 가능합니다.
        """
        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "Django 스터디그룹입니다.",
            "study_name": "Django 스터디",
            # 오늘보다 일주일 뒤
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=14),
            "deadline": date.today() + timedelta(days=3),
            "member_limit": 10,
            "categories": "Django",
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 1, f"response: {response.data}")

    def test_create_without_head_image(self):
        """
        head_image가 없는 경우, default_head_image가 반환됩니다.
        """
        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "Django 스터디그룹입니다.",
            "study_name": "Django 스터디",
            # 오늘보다 일주일 뒤
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=14),
            "deadline": date.today() + timedelta(days=3),
            "member_limit": 10,
            "categories": "Django",
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 1, f"response: {response.data}")
        self.assertEqual(
            response.data["head_image"], StudyGroup.objects.first().default_head_image
        )

    def test_create_with_head_image(self):
        """
        head_image가 있는 경우, 해당 이미지가 반환됩니다.
        """
        url = reverse("studygroup_list")
        data = {
            # file
            "head_image": open("apps/studygroup/tests/test_image.png", "rb"),
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "Django 스터디그룹입니다.",
            "study_name": "Django 스터디",
            # 오늘보다 일주일 뒤
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=14),
            "deadline": date.today() + timedelta(days=3),
            "member_limit": 10,
            "categories": "Django",
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 1, f"response: {response.data}")
        self.assertEqual(
            response.data["head_image"].split("/")[-1],
            data["head_image"].name.split("/")[-1],
        )

    def test_create_invalid_date(self):
        """
        스터디그룹 모집 마감일은 오늘보다 미래여야 합니다.
        """
        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "Django 스터디그룹입니다.",
            "study_name": "Django 스터디",
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=14),
            "deadline": date.today() - timedelta(days=3),  # 오늘보다 과거
            "member_limit": 10,
            "categories": "Django",
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 0, f"response: {response.data}")
