from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User

REFRESH_API_URL_NAME = "token_refresh"


class TokenRefreshTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            username="test",
            password="test",
        )

    def test_token_refresh(self):
        """
        Token Refresh API 를 통해 access token 을 새로 발급받을 수 있어야 합니다.
        """
        refresh_token = RefreshToken.for_user(self.user)
        response = self.client.post(
            path=reverse(REFRESH_API_URL_NAME),
            data={"refresh": str(refresh_token)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
