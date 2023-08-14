from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from studygroup.models import Category


class CategoryTestCase(APITestCase):
    def setUp(self) -> None:
        for category_name in ["백엔드", "프론트엔드", "데브옵스"]:
            Category.objects.create(name=category_name)

    def test_create_account(self):
        url = reverse("category_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(
            response.data, [{"name": "백엔드"}, {"name": "프론트엔드"}, {"name": "데브옵스"}]
        )


class StudyGroupTestCase(APITestCase):
    def setUp(self):
        for i in range(30):
            User.objects.create(
                email=f"user-{i}@example.com",
                username=f"user-{i}",
                password=f"password-{i}",
            )
