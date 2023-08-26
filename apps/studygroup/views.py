from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from apps.studygroup import models, serializers
from apps.studygroup.filters import StudyGroupFilter
from apps.studygroup.pagination import StudyGroupPagination


@extend_schema(tags=["스터디그룹 API"])
class StudyGroupAPISet(viewsets.ModelViewSet):
    # Serializer
    serializer_class = serializers.StudyGroupListSerializer

    # Parser
    parser_classes = (MultiPartParser, FormParser)

    # Lookup Field
    lookup_field = "uuid"

    # Permission
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # Ordering
    ordering_fields = ["created_at", "deadline"]

    # Filtering
    queryset = models.StudyGroup.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = StudyGroupFilter

    # Pagination
    pagination_class = StudyGroupPagination

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return serializers.StudyGroupListSerializer
        # elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
        #     return serializers.StudyGroupDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        print(serializer.instance)
        initial_member = models.StudyGroupMember.objects.create(
            user=self.request.user, study_group=serializer.instance, is_leader=True
        )
        serializer.instance.members.add(initial_member)

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
        pass

    @extend_schema(summary="특정 스터디그룹을 삭제합니다.")
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)


@extend_schema(tags=["카테고리 API"])
class CategoryListAPI(generics.ListAPIView):
    pagination_class = None
    permission_classes = (AllowAny,)
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    @extend_schema(summary="카테고리 목록을 조회합니다.")
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)
