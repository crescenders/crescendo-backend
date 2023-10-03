from typing import Any

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.registration.views import SocialLoginView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenBlacklistView as _TokenBlacklistView
from rest_framework_simplejwt.views import TokenRefreshView as _TokenRefreshView

from apps.accounts.models import User
from apps.accounts.serializers import GoogleLoginSerializer, ProfileSerializer
from apps.studygroup.filters import MyStudyGroupFilter
from apps.studygroup.models import StudyGroup
from apps.studygroup.pagination import StudyGroupPagination
from apps.studygroup.serializers import StudyGroupListSerializer


class TokenRefreshAPI(_TokenRefreshView):  # type: ignore
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
        return super().post(request, *args, **kwargs)  # type: ignore


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


@extend_schema(
    tags=["로그인/로그아웃 API"],
    summary="로그아웃합니다. refresh token 을 blacklist 에 추가합니다.",
)
class LogoutAPI(_TokenBlacklistView):  # type: ignore
    """
    로그아웃에 사용된 refresh token 은 더 이상 사용될 수 없습니다.
    """

    pass


@extend_schema(
    tags=["사용자 정보 API"],
)
# class MyProfileAPI(generics.RetrieveUpdateDestroyAPIView[User]):
class MyProfileAPI(generics.RetrieveUpdateAPIView):
    """
    로그인한 사용자의 정보를 조회/수정/탈퇴합니다.
    """

    http_method_names = ["get", "put", "delete"]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self) -> User:
        queryset = self.get_queryset()
        assert type(self.request.user) is User
        obj = get_object_or_404(queryset, uuid=self.request.user.uuid)
        assert isinstance(obj, User)
        return obj

    @extend_schema(summary="로그인한 사용자의 정보를 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="로그인한 사용자의 정보를 수정합니다.")
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().put(request, *args, **kwargs)

    @extend_schema(summary="로그인한 사용자를 탈퇴 처리합니다.")
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().delete(request, *args, **kwargs)  # TODO: 탈퇴 처리


@extend_schema(
    tags=["사용자 정보 API"],
)
class MyStudyAPI(mixins.ListModelMixin, generics.GenericAPIView):
    """
    로그인한 사용자와 관련된 스터디 그룹을 조회합니다.
    """

    # serializer
    serializer_class = StudyGroupListSerializer

    # pagination
    pagination_class = StudyGroupPagination

    # queryset
    queryset = StudyGroup.objects.all()

    # filtering
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MyStudyGroupFilter

    @extend_schema(summary="로그인한 사용자가 가입한 스터디 그룹을 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.list(request, *args, **kwargs)


@extend_schema(
    tags=["사용자 정보 API"],
)
class UUIDProfileAPI(generics.RetrieveAPIView):
    """
    UUID를 이용하여 사용자의 정보를 조회합니다.
    """

    lookup_field = "uuid"
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    @extend_schema(summary="UUID를 이용하여 사용자의 정보를 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
