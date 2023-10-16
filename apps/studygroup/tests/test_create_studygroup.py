from datetime import timedelta

from django.utils.datetime_safe import date
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.models import StudyGroup, Tag
from apps.studygroup.tests.factories import CategoryFactory, UserFactory


class CreateStudyGroupTestCase(APITestCase):
    def setUp(self) -> None:
        CategoryFactory(name="Django")
        CategoryFactory(name="React")
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

    def test_deadline_is_future(self):
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

    def test_start_date_is_bigger_than_deadline(self):
        """
        스터디그룹 시작일은 모집 마감일보다 뒤여야 합니다.
        """
        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "Django 스터디그룹입니다.",
            "study_name": "Django 스터디",
            "start_date": date.today() + timedelta(days=7),  # 모집 마감일보다 일찍
            "end_date": date.today() + timedelta(days=14),
            "deadline": date.today() + timedelta(days=10),
            "member_limit": 10,
            "categories": "Django",
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 0, f"response: {response.data}")

    def test_end_date_is_bigger_than_start_date(self):
        """
        스터디그룹 종료일은 시작일보다 뒤여야 합니다.
        """
        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "Django 스터디그룹입니다.",
            "study_name": "Django 스터디",
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=3),  # 시작일보다 일찍
            "deadline": date.today() + timedelta(days=10),
            "member_limit": 10,
            "categories": "Django",
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 0, f"response: {response.data}")

    def test_member_limit_is_between_2_and_10(self):
        """
        스터디그룹 인원 제한은 2명 이상 10명 이하여야 합니다.
        """
        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "Django 스터디그룹입니다.",
            "study_name": "Django 스터디",
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=10),
            "deadline": date.today() + timedelta(days=3),
            "member_limit": 1,  # 2명 미만
            "categories": "Django",
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 0, f"response: {response.data}")

        data["member_limit"] = 11  # 10명 초과
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 0, f"response: {response.data}")

    def test_categories_is_required(self):
        """
        스터디그룹 카테고리는 필수입니다.
        """
        url = reverse("studygroup_list")
        # 카테고리 없이 요청
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "Django 스터디그룹입니다.",
            "study_name": "Django 스터디",
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=10),
            "deadline": date.today() + timedelta(days=3),
            "member_limit": 5,
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 0, f"response: {response.data}")

    def test_formdata_category_is_required(self):
        """
        formdata 로 여러 개의 카테고리를 생성하도록 요청할 때, 아래의 형식이어야 합니다.

        categories = "Django"
        categories = "React"
        """

        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "Django 스터디그룹입니다.",
            "study_name": "Django 스터디",
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=10),
            "deadline": date.today() + timedelta(days=3),
            "member_limit": 5,
            "categories": ["Django", "React"],
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data, format="multipart")
        self.assertEqual(response.status_code, 201, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 1, f"response: {response.data}")

    def test_tag_can_be_empty(self):
        """
        스터디그룹 태그는 비워둘 수 있습니다.
        """
        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "Django 스터디그룹입니다.",
            "study_name": "Django 스터디",
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=10),
            "deadline": date.today() + timedelta(days=3),
            "member_limit": 5,
            "categories": "Django",
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 1, f"response: {response.data}")

    def test_tag_get(self):
        """
        이미 존재하는 태그를 요청하면, 새로운 태그를 생성하지 않습니다.
        """
        Tag.objects.create(name="some_tag")
        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "React 스터디그룹입니다.",
            "study_name": "React 스터디",
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=10),
            "deadline": date.today() + timedelta(days=3),
            "member_limit": 5,
            "categories": "React",
            "tags": "some_tag",
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 1, f"response: {response.data}")
        self.assertEqual(Tag.objects.count(), 1, f"response: {response.data}")

    def test_tag_get_or_create(self):
        """
        스터디그룹 태그는 존재하지 않는 태그를 요청하면 생성됩니다.
        """
        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "React 스터디그룹입니다.",
            "study_name": "React 스터디",
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=10),
            "deadline": date.today() + timedelta(days=3),
            "member_limit": 5,
            "categories": "React",
            "tags": "some_tag",
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 1, f"response: {response.data}")
        self.assertEqual(Tag.objects.count(), 1, f"response: {response.data}")

    def test_create_with_tags(self):
        """
        스터디그룹 생성 시 태그를 여러 개 생성할 수 있습니다.
        """
        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "React 스터디그룹입니다.",
            "study_name": "React 스터디",
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=10),
            "deadline": date.today() + timedelta(days=3),
            "member_limit": 5,
            "categories": "React",
            "tags": ["some_tag", "some_tag2"],
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data, format="multipart")
        self.assertEqual(response.status_code, 201, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 1, f"response: {response.data}")
        self.assertEqual(Tag.objects.count(), 2, f"response: {response.data}")
        self.assertEqual(response.data["tags"][0], data["tags"][0])
        self.assertEqual(response.data["tags"][1], data["tags"][1])

    def test_auto_registered_as_leader(self):
        """
        스터디그룹 개설자는 자동으로 스터디그룹장이 됩니다.
        """
        url = reverse("studygroup_list")
        data = {
            "post_title": "스터디그룹 개설합니다.",
            "post_content": "Django 스터디그룹입니다.",
            "study_name": "Django 스터디",
            "start_date": date.today() + timedelta(days=7),
            "end_date": date.today() + timedelta(days=10),
            "deadline": date.today() + timedelta(days=3),
            "member_limit": 5,
            "categories": "Django",
        }
        self.client.force_authenticate(user=self.logged_in_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201, f"response: {response.data}")
        self.assertEqual(StudyGroup.objects.count(), 1, f"response: {response.data}")
        self.assertEqual(
            StudyGroup.objects.first().leaders.first().user, self.logged_in_user
        )
