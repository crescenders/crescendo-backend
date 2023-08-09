from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from studygroup import models, serializers


@extend_schema(tags=["스터디그룹 API"])
class StudyGroupAPISet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    permission_classes = (AllowAny,)
    queryset = models.StudyGroup.objects.all()
    serializer_class = serializers.StudyGroupSerializer


@extend_schema(tags=["카테고리 API"])
class CategoryListAPI(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    @extend_schema(summary="카테고리 목록을 조회합니다.")
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)
