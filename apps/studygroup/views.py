from typing import Any

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from apps.studygroup import models, serializers


@extend_schema(tags=["스터디그룹 API"])
class StudyGroupAPISet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.StudyGroup.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = serializers.StudyGroupListSerializer

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return serializers.StudyGroupListSerializer
        # elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
        #     return serializers.StudyGroupDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.validated_data["leader"] = self.request.user
        return super().perform_create(serializer)

    @extend_schema(summary="스터디그룹 홍보글 목록을 조회합니다.")
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="새로운 스터디그룹을 개설합니다.")
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="retrieve")
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="update")
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pass

    @extend_schema(summary="delete")
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)


@extend_schema(tags=["카테고리 API"])
class CategoryListAPI(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    @extend_schema(summary="카테고리 목록을 조회합니다.")
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)
