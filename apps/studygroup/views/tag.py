from typing import Any

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.studygroup.models import Tag
from apps.studygroup.serializers import TagReadSerializer


@extend_schema(
    tags=["스터디그룹 태그 API"],
    summary="스터디그룹 태그 목록을 조회합니다.",
    parameters=[
        OpenApiParameter(
            name="random_count",
            description="목록 조회 시, 얼만큼의 태그를 랜덤으로 보여줄지 결정합니다.",
            required=True,
            type={
                "type": "integer",
                "minimum": 1,
                "maximum": 10,
            },
            location=OpenApiParameter.QUERY,
            default=3,
            explode=False,
        )
    ],
)
class TagRandomListAPI(ListAPIView):
    """
    querystring에 전달된 숫자만큼의 랜덤 태그를 반환합니다.
    """

    queryset = Tag.objects.filter(studygroups__isnull=False)
    serializer_class = TagReadSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        random_count = int(self.request.query_params.get("random_count", 3))
        return self.queryset.order_by("?")[:random_count]

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        self._validate_random_count(
            random_count=request.query_params.get("random_count", 3)
        )
        return super().list(request, *args, **kwargs)

    @staticmethod
    def _validate_random_count(random_count: int) -> int:
        try:
            random_count = int(random_count)
        except ValueError:
            raise ValidationError(detail={"random_count": "숫자만 입력할 수 있습니다."})

        if random_count < 1 or random_count > 10:
            raise ValidationError(
                detail={"random_count": "최소 1개, 최대 10개의 태그만 랜덤으로 조회할 수 있습니다."}
            )

        return random_count
