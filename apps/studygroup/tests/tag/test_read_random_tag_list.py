import factory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.studygroup.tests.factories import TagFactory


class TagTestCase(APITestCase):
    def setUp(self):
        TagFactory.create_batch(10, name=factory.Faker("uuid4"))

    def test_read_random_tags_default_is_3(self):
        """
        기본적으로 3개의 태그를 랜덤으로 반환합니다.
        """
        url = reverse("tag-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_read_random_tags_with_querystring(self):
        """
        querystring에 전달된 숫자만큼의 랜덤 태그를 반환합니다.
        """
        url = reverse("tag-list")
        response = self.client.get(url, {"random_count": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_read_random_tags_with_querystring_out_of_minimum_range(self):
        """
        querystring에 전달된 숫자가 범위를 벗어나면, 400 에러를 반환합니다.
        """
        url = reverse("tag-list")
        response = self.client.get(url, {"random_count": 11})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
