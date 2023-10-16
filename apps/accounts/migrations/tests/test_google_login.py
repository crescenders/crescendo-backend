from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


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
