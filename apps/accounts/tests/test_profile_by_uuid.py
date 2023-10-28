from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.accounts.urls import AccountsURLs


class ProfileAPIByUUIDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            username="test",
            password="test",
        )

    def test_read_profile_by_uuid(self):
        """
        UUID 기반 유저 정보 조회 API 테스트
        """
        response = self.client.get(
            path=reverse(
                AccountsURLs.UUID_PROFILE, kwargs={"user_uuid": str(self.user.uuid)}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uuid"], str(self.user.uuid))
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["username"], self.user.username)
