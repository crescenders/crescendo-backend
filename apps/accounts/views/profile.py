from typing import Any

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.accounts.models import User
from apps.accounts.serializers import ProfileSerializer
from apps.studygroup.filters import MyStudyGroupFilter
from apps.studygroup.models import StudyGroup
from apps.studygroup.pagination import StudyGroupPagination
from apps.studygroup.serializers import MyStudyGroupReadSerializer


@extend_schema(
    tags=["사용자 정보 API"],
)
class MyProfileAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    로그인한 사용자의 정보를 조회/수정/탈퇴합니다.
    """

    http_method_names = ["get", "put", "delete"]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self) -> User:
        queryset = self.get_queryset()
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
        return super().delete(request, *args, **kwargs)


@extend_schema(
    tags=["사용자 정보 API"],
)
class MyStudyAPI(mixins.ListModelMixin, generics.GenericAPIView[StudyGroup]):
    """
    로그인한 사용자와 관련된 스터디 그룹을 조회합니다.
    """

    serializer_class = MyStudyGroupReadSerializer
    pagination_class = StudyGroupPagination
    queryset = StudyGroup.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MyStudyGroupFilter

    def get_queryset(self) -> QuerySet[StudyGroup]:
        return self.queryset.defer("content")

    @extend_schema(summary="로그인한 사용자가 가입한 스터디 그룹을 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.list(request, *args, **kwargs)


@extend_schema(
    tags=["사용자 정보 API"],
)
class UUIDProfileAPI(generics.RetrieveAPIView[User]):
    """
    UUID를 이용하여 사용자의 정보를 조회합니다.
    """

    lookup_field = "uuid"
    lookup_url_kwarg = "user_uuid"
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    @extend_schema(summary="UUID를 이용하여 사용자의 정보를 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
