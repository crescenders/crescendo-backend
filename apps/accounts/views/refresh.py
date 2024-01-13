from typing import Any

from dj_rest_auth.app_settings import api_settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView as _TokenRefreshView


class TokenRefreshAPI(_TokenRefreshView):
    """
    클라이언트가 가지고 있는 refresh token 을 이용하여 새로운 access token 을 발급합니다.
    """

    @extend_schema(
        tags=["로그인/로그아웃 API"],
        summary="클라이언트가 가지고 있는 refresh token 을 이용하여 새로운 access token 을 발급합니다.",
        responses={
            status.HTTP_200_OK: api_settings.JWT_SERIALIZER,
        },
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().post(request, *args, **kwargs)
