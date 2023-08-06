from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client, OAuth2Error
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.registration.views import SocialLoginView
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView as _TokenRefreshView

from accounts.models import User
from accounts.serializers import GoogleLoginSerializer, UserSerializer
from core.exceptions.serailizers import InvalidTokenExceptionSerializer


class TokenRefreshView(_TokenRefreshView):
    """
    클라이언트가 가지고 있는 refresh token 을 이용하여 새로운 access token 을 발급합니다.
    """

    @extend_schema(
        tags=["로그인 API"],
        summary="클라이언트가 가지고 있는 refresh token 을 이용하여 새로운 access token 을 발급합니다.",
        responses={
            status.HTTP_200_OK: api_settings.JWT_SERIALIZER,
            status.HTTP_401_UNAUTHORIZED: InvalidTokenExceptionSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class GoogleLogin(SocialLoginView):
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
        tags=["로그인 API"],
        summary="Google 로부터 얻은 액세스 토큰을 이용하여 Crescendo 서비스의 JWT 를 발급합니다.",
        responses={
            status.HTTP_200_OK: api_settings.JWT_SERIALIZER,
            status.HTTP_401_UNAUTHORIZED: InvalidTokenExceptionSerializer,
        },
        external_docs="https://developers.google.com/identity/gsi/web/guides/overview?hl=ko",
    )
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except OAuth2Error:
            raise InvalidToken


class KakaoLogin(SocialLoginView):
    """
    Kakao Login API 입니다. 현재 개발 중입니다.
    """

    adapter_class = KakaoOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = OAuth2Client

    @extend_schema(
        tags=["로그인 API"],
        summary="Kakao Login API 입니다. 현재 개발 중입니다.",
        deprecated=True,
        responses={
            status.HTTP_200_OK: api_settings.JWT_SERIALIZER,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    tags=["내 정보 API"],
)
class ProfileAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    로그인한 사용자의 정보를 조회/수정/탈퇴합니다.
    """

    http_method_names = ["get", "put", "delete"]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, uuid=self.request.user.uuid)
        return obj

    @extend_schema(summary="로그인한 사용자의 정보를 조회합니다.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="로그인한 사용자의 정보를 수정합니다.")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(summary="로그인한 사용자를 탈퇴 처리합니다.")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
