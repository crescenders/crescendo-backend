from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User

GOOGLE_LOGIN_API_URL_NAME = "google_login"
REFRESH_API_URL_NAME = "token_refresh"
LOGOUT_API_URL_NAME = "token_blacklist"


class GoogleLoginTestCase(APITestCase):
    def test_invalid_google_login(self):
        """
        유효하지 않은 Google access token 으로 Google Login API 를 호출하면 400 응답을 받아야 합니다.
        """
        response = self.client.post(
            path=reverse("google_login"),
            data={"access": "invalid_access_token"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("code", response.data)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["code"], "token_not_valid")
        self.assertEqual(response.data["detail"], "Token is invalid or expired")


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

    def test_invalid_refresh_token_refresh(self):
        """
        유효하지 않은 토큰으로 Token Refresh API 를 호출하면 401 응답을 받아야 합니다.
        """
        response = self.client.post(
            path=reverse(REFRESH_API_URL_NAME),
            data={"refresh": "invalid_token"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("code", response.data)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["code"], "token_not_valid")
        self.assertEqual(response.data["detail"], "Token is invalid or expired")

    def test_refresh_token_rotation_fails(self):
        """
        한 번 사용한 refresh token 으로 Token Refresh API 를 호출하면 401 응답을 받아야 합니다.
        """
        refresh_token = RefreshToken.for_user(self.user)
        response = self.client.post(
            path=reverse(REFRESH_API_URL_NAME),
            data={"refresh": str(refresh_token)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            path=reverse(REFRESH_API_URL_NAME),
            data={"refresh": str(refresh_token)},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("code", response.data)
        self.assertIn("detail", response.data)


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
            path=reverse(LOGOUT_API_URL_NAME),
            data={"refresh": str(refresh_token)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            path=reverse(REFRESH_API_URL_NAME),
            data={"refresh": str(refresh_token)},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("code", response.data)
        self.assertIn("detail", response.data)
