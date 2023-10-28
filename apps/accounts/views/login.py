from typing import Any

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.registration.views import SocialLoginView
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken

from apps.accounts.serializers import GoogleLoginSerializer


class GoogleLoginAPI(SocialLoginView):  # type: ignore
    """
    Google Login API 입니다. Google 로부터 얻은 액세스 토큰을 이용하여 Crescendo 서비스의 JWT 를 발급합니다.

    Crescendo 서비스 JWT 의 payload 를 디코딩하면 아래와 같은 형태입니다.
    ```json
    {
      "token_type": "refresh",
      "exp": 1691849064,
      "iat": 1691244264,
      "jti": "52ca4fe0f90b4d7783e80b7ec30e95c9",
      "user_uuid": "bcbdad4c-1e13-4087-b5e9-628599d32d5a"
    }
    ```
    """

    serializer_class = GoogleLoginSerializer
    adapter_class = GoogleOAuth2Adapter

    @extend_schema(
        tags=["로그인/로그아웃 API"],
        summary="Google 로부터 얻은 액세스 토큰을 이용하여 Crescendo 서비스의 JWT 를 발급합니다.",
        responses={
            status.HTTP_200_OK: api_settings.JWT_SERIALIZER,
        },
        external_docs=(
            "https://developers.google.com/identity/gsi/web/guides/overview?hl=ko"
        ),
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            return super().post(request, *args, **kwargs)  # type: ignore
        except OAuth2Error:
            raise InvalidToken
