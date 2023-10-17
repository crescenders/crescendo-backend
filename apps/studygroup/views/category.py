from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.studygroup.models import Category
from apps.studygroup.serializers import CategoryReadSerializer


@extend_schema(tags=["카테고리 API"])
class CategoryListAPI(generics.ListAPIView):
    pagination_class = None
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer

    @extend_schema(summary="카테고리 목록을 조회합니다.")
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
