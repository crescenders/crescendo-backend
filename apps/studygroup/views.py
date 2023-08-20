from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.studygroup import models, serializers


@extend_schema(tags=["스터디그룹 API"])
class StudyGroupAPISet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    permission_classes = (AllowAny,)
    queryset = models.StudyGroup.objects.all()
    serializer_class = serializers.StudyGroupSerializer

    @extend_schema(summary="스터디그룹 홍보글 목록을 조회합니다.")
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="create")
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
