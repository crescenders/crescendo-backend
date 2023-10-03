from typing import Any

from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from apps.accounts.models import User
from apps.studygroup.filters import StudyGroupListFilter
from apps.studygroup.models import Category, StudyGroup, StudyGroupMember
from apps.studygroup.pagination import StudyGroupPagination
from apps.studygroup.permissions import IsLeaderOrReadOnly
from apps.studygroup.serializers import (
    CategorySerializer,
    StudyGroupDetailSerializer,
    StudyGroupListSerializer,
)


@extend_schema(tags=["스터디그룹 API"])
class StudyGroupAPISet(viewsets.ModelViewSet):
    # Serializer
    serializer_class = StudyGroupListSerializer

    # Parser
    parser_classes = (MultiPartParser, FormParser)

    # Lookup Field
    lookup_field = "uuid"

    # Permission
    permission_classes = (IsLeaderOrReadOnly,)

    # Filtering
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StudyGroupListFilter

    # Pagination
    pagination_class = StudyGroupPagination

    def get_queryset(self) -> QuerySet[StudyGroup]:
        queryset = StudyGroup.objects.all()
        if self.action in ["list"]:
            return queryset.defer("content")
        return queryset

    def get_serializer_class(self) -> type[BaseSerializer[StudyGroup]]:
        if self.action in ["list", "create"]:
            return StudyGroupListSerializer
        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return StudyGroupDetailSerializer
        return super().get_serializer_class()

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
            study_group=serializer.instance,
            is_leader=True,
            is_approved=True,
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

    @extend_schema(summary="특정 스터디그룹을 삭제합니다.")
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["카테고리 API"])
class CategoryListAPI(generics.ListAPIView):
    pagination_class = None
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(summary="카테고리 목록을 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
