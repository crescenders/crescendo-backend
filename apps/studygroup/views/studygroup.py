from typing import Any, Sequence

from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from apps.accounts.models import User
from apps.studygroup.filters import StudyGroupListFilter, StudyGroupOrderingFilter
from apps.studygroup.models import StudyGroup, StudyGroupMember
from apps.studygroup.pagination import StudyGroupPagination
from apps.studygroup.permissions import (
    StudyGroupCreatePermission,
    StudyGroupDeleteOrUpdatePermission,
)
from apps.studygroup.serializers import (
    StudyGroupDetailSerializer,
    StudyGroupListSerializer,
)


@extend_schema(tags=["스터디그룹 관리 API"])
class StudyGroupAPISet(viewsets.ModelViewSet):
    serializer_class = StudyGroupListSerializer
    serializer_classes = {
        "list": StudyGroupListSerializer,
        "create": StudyGroupListSerializer,
        "retrieve": StudyGroupDetailSerializer,
        "update": StudyGroupDetailSerializer,
    }
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = "uuid"
    permission_classes = (AllowAny,)
    filter_backends = (
        DjangoFilterBackend,
        StudyGroupOrderingFilter,
    )
    filterset_class = StudyGroupListFilter
    pagination_class = StudyGroupPagination
    ordering = ("-created_at",)

    def get_permissions(self) -> Sequence[BasePermission]:
        """
        스터디그룹을 생성할 때, 스터디그룹장이 되는 유저는 스터디그룹장 권한을 가지고 있어야 합니다.
        """
        if self.action == "create":
            return [permission() for permission in [StudyGroupCreatePermission]]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [permission() for permission in [StudyGroupDeleteOrUpdatePermission]]
        return super().get_permissions()

    def get_queryset(self) -> QuerySet[StudyGroup]:
        queryset = StudyGroup.objects.all()
        if self.action in ["list"]:
            return queryset.defer("content")
        return queryset

    def get_serializer_class(self) -> type[BaseSerializer[StudyGroup]]:
        return self.serializer_classes.get(self.action, self.serializer_class)

    @transaction.atomic
    def perform_create(self, serializer: BaseSerializer[StudyGroup]) -> None:
        """
        스터디그룹을 생성하면, 스터디그룹장으로 자동으로 등록됩니다.
        """
        super().perform_create(serializer)
        assert isinstance(self.request.user, User)
        assert isinstance(serializer.instance, StudyGroup)
        initial_member = StudyGroupMember.objects.create(
            user=self.request.user,
            studygroup=serializer.instance,
            is_leader=True,
        )
        serializer.instance.members.add(initial_member)

    @transaction.atomic
    def perform_update(self, serializer: BaseSerializer[StudyGroup]) -> None:
        """
        formdata 의 head_image 가 빈 값이면, 이미지를 삭제하고 빈 값으로 저장합니다.
        """
        assert serializer.instance is not None
        if self.request.data.get("head_image") == "":
            serializer.instance.head_image.delete()
            serializer.instance.head_image = None
        super().perform_update(serializer)

    @extend_schema(summary="스터디그룹 홍보글 목록을 조회합니다.")
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="새로운 스터디그룹을 개설합니다.")
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="특정 스터디그룹 상세 정보를 조회합니다.")
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 정보를 수정합니다.")
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 정보를 일부 수정합니다.", deprecated=True)
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary="특정 스터디그룹을 삭제합니다.")
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)
