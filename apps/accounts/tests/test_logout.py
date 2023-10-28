from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from apps.accounts.urls import AccountsURLs


class LogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            username="test",
            password="test",
        )

    def test_logout(self):
        """
        한 번 로그아웃을 하고 나면, 로그아웃을 위해 사용된 refresh token 으로는 Token Refresh API 호출이 불가능해야 합니다.
        """
        refresh_token = RefreshToken.for_user(self.user)
        response = self.client.post(
            path=reverse(AccountsURLs.LOGOUT),
            data={"refresh": str(refresh_token)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            path=reverse(AccountsURLs.REFRESH_LOGIN),
            data={"refresh": str(refresh_token)},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("code", response.data)
        self.assertIn("detail", response.data)
