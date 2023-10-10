from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.models import Category
from apps.studygroup.tests.factories import CategoryFactory


class CategoryTestCase(APITestCase):
    """
    카테고리 API 테스트
    """

    def setUp(self) -> None:
        CategoryFactory(name="백엔드")
        CategoryFactory(name="프론트엔드")
        CategoryFactory(name="데브옵스")

    def test_read_categories(self):
        url = reverse("category_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(
            response.data,
            [
                {"name": "백엔드"},
                {"name": "프론트엔드"},
                {"name": "데브옵스"},
            ],
        )
