from django.db.models import QuerySet
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.studygroup.models import StudyGroupAssignmentRequest
from apps.studygroup.serializers import StudyGroupAssignmentReadSerializer


@extend_schema(tags=["스터디그룹 과제 관리 API"])
class StudyGroupAssignmentRequestAPISet(viewsets.ModelViewSet):
    """
    스터디그룹 과제 관리 API
    """

    permission_classes = (AllowAny,)
    queryset = StudyGroupAssignmentRequest.objects.all()
    serializer_class = StudyGroupAssignmentReadSerializer

    def get_queryset(self) -> QuerySet[StudyGroupAssignmentRequest]:
        studygroup_uuid = self.kwargs.get("uuid")
        return self.queryset.filter(studygroup__uuid=studygroup_uuid)

    @extend_schema(
        summary="스터디그룹 과제 목록을 조회합니다.",
        parameters=[
            OpenApiParameter(
                name="truncate",
                description="목록 조회 시, 얼만큼의 내용을 잘라서 보여줄지 결정합니다. 최대 150자까지 가능합니다.",
                type={
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 150,
                },
                location=OpenApiParameter.QUERY,
                required=False,
                default=20,
                explode=False,
            )
        ],
    )
    def list(self, request, *args, **kwargs) -> Response:
        """
        - 멤버가 아닌 사람은 과제의 제목만 조회할 수 있습니다.
        - 멤버인 사람은 과제의 제목, 내용을 조회할 수 있습니다.
        """
        queryset = self.filter_queryset(self.get_queryset())
        truncate = int(request.query_params.get("truncate", 20))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        # 스터디그룹의 멤버일 경우, 과제의 내용을 일부 볼 수 있습니다.
        # 과제의 내용이 길 경우, 일부만 보여줍니다.
        users = [member.user for member in queryset.first().studygroup.members.all()]
        if request.user in users:
            for data in serializer.data:
                if len(data["content"]) > truncate:
                    data["content"] = data["content"][:truncate] + "..."
                else:
                    data["content"] = data["content"][:truncate]

        # 스터디그룹의 멤버가 아니거나 로그인 하지 않은 경우, 과제의 내용을 볼 수 없습니다.
        # content 필드를 빈 문자열로 바꿔줍니다.
        else:
            for data in serializer.data:
                data["content"] = ""

        return Response(serializer.data)

    @extend_schema(summary="스터디그룹 과제를 생성합니다.")
    def create(self, request, *args, **kwargs) -> Response:
        """
        - 스터디그룹의 리더만 과제를 생성할 수 있습니다.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 과제를 상세 조회합니다.")
    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        상세 조회는 스터디그룹의 멤버만 가능합니다.
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 과제를 수정합니다.", deprecated=True)
    def update(self, request, *args, **kwargs) -> Response:
        """
        - 스터디그룹의 리더만 과제를 수정할 수 있습니다.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 과제를 부분 수정합니다.", deprecated=True)
    def partial_update(self, request, *args, **kwargs) -> Response:
        """
        - 스터디그룹의 리더만 과제를 부분 수정할 수 있습니다.
        """
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 과제를 삭제합니다.")
    def destroy(self, request, *args, **kwargs) -> Response:
        """
        - 스터디그룹의 리더만 과제를 삭제할 수 있습니다.
        """
        return super().destroy(request, *args, **kwargs)
