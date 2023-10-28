from django.db.models import QuerySet
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from apps.studygroup.models import (
    AssignmentRequest,
    AssignmentSubmission,
    StudyGroup,
    StudyGroupMember,
)
from apps.studygroup.pagination import StudyGroupAssignmentPagination
from apps.studygroup.permissions import IsLeaderOrReadOnlyForAssignment
from apps.studygroup.serializers import (
    StudyGroupAssignmentCreateSerializer,
    StudyGroupAssignmentReadSerializer,
    StudyGroupAssignmentSubmissionCreateSerializer,
    StudyGroupAssignmentSubmissionReadSerializer,
)


@extend_schema(tags=["스터디그룹 과제 등록 관리 API"])
class StudyGroupAssignmentRequestAPISet(viewsets.ModelViewSet):
    """
    스터디그룹 과제 관리 API
    """

    lookup_url_kwarg = "assignment_id"
    permission_classes = (IsLeaderOrReadOnlyForAssignment,)
    queryset = AssignmentRequest.objects.all()
    serializer_class = StudyGroupAssignmentReadSerializer
    serializer_classes = {
        "list": StudyGroupAssignmentReadSerializer,
        "create": StudyGroupAssignmentCreateSerializer,
        "retrieve": StudyGroupAssignmentReadSerializer,
        "update": StudyGroupAssignmentCreateSerializer,
    }
    pagination_class = StudyGroupAssignmentPagination

    def get_queryset(self) -> QuerySet[AssignmentRequest]:
        studygroup_uuid = self.kwargs.get("studygroup_uuid")
        return self.queryset.filter(studygroup__uuid=studygroup_uuid)

    def get_serializer_class(self) -> BaseSerializer[AssignmentRequest]:
        return self.serializer_classes.get(self.action, self.serializer_class)

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
        if self._check_user_is_member(request):
            serializer = self.get_serializer(page, many=True)
            for data in serializer.data:
                data["content"] = self._get_truncate_content(data["content"], truncate)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(page, many=True)
            for data in serializer.data:
                data["content"] = self._get_empty_content(data["content"])
            return self.get_paginated_response(serializer.data)

    @extend_schema(summary="스터디그룹 과제를 생성합니다.")
    def create(self, request, *args, **kwargs) -> Response:
        """
        스터디그룹의 리더만 과제를 생성할 수 있습니다.
        """
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer) -> None:
        studygroup_uuid = self.kwargs.get("studygroup_uuid")
        studygroup = StudyGroup.objects.get(uuid=studygroup_uuid)
        author = StudyGroupMember.objects.get(
            studygroup=studygroup, user=self.request.user
        )
        serializer.save(author=author, studygroup=studygroup)

    @extend_schema(summary="스터디그룹 과제를 상세 조회합니다.")
    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        상세 조회는 스터디그룹의 멤버만 가능합니다.
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 과제를 수정합니다.")
    def update(self, request, *args, **kwargs) -> Response:
        """
        - 스터디그룹의 리더만 과제를 수정할 수 있습니다.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 과제를 부분 수정합니다.")
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

    def _check_user_is_member(self, request) -> bool:
        """
        멤버인지 확인합니다.
        """
        studygroup_uuid = self.kwargs.get("studygroup_uuid")
        studygroup = StudyGroup.objects.get(uuid=studygroup_uuid)
        users = [member.user for member in studygroup.members.all()]
        if request.user in users:
            return True
        return False

    @staticmethod
    def _get_truncate_content(content: str, truncate: int) -> str:
        """
        content를 truncate 길이만큼 자릅니다.
        """
        if len(content) > truncate:
            return content[:truncate] + "..."
        return content[:truncate]

    @staticmethod
    def _get_empty_content(content: str) -> str:
        """
        content를 비웁니다.
        단순히 빈 문자열을 리턴하지만, 이후에 다른 로직이 추가될 수 있으므로 메서드로 분리합니다.
        """
        return ""


@extend_schema(tags=["스터디그룹 과제 제출 관리 API"])
class StudyGroupAssignmentSubmissionAPISet(viewsets.ModelViewSet):
    """
    스터디그룹 과제 제출 관리 API
    """

    lookup_url_kwarg = "submission_id"
    queryset = AssignmentSubmission.objects.all()
    serializer_class = StudyGroupAssignmentSubmissionReadSerializer
    serializer_classes = {
        "list": StudyGroupAssignmentSubmissionReadSerializer,
        "create": StudyGroupAssignmentSubmissionCreateSerializer,
    }
    pagination_class = StudyGroupAssignmentPagination

    def get_queryset(self) -> QuerySet[AssignmentSubmission]:
        studygroup_uuid = self.kwargs.get("studygroup_uuid")
        return self.queryset.filter(studygroup__uuid=studygroup_uuid)

    def get_serializer_class(self) -> BaseSerializer[AssignmentSubmission]:
        return self.serializer_classes.get(self.action, self.serializer_class)

    @extend_schema(summary="스터디그룹 과제 제출 목록을 조회합니다.")
    def list(self, request, *args, **kwargs) -> Response:
        """
        스터디그룹의 멤버만 제출된 과제들을 조회할 수 있습니다.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 과제 제출을 생성합니다.")
    def create(self, request, *args, **kwargs) -> Response:
        """
        스터디그룹의 멤버만 과제를 제출할 수 있습니다.
        """
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer) -> None:
        studygroup_uuid = self.kwargs.get("studygroup_uuid")
        studygroup = StudyGroup.objects.get(uuid=studygroup_uuid)
        author = StudyGroupMember.objects.get(
            studygroup=studygroup, user=self.request.user
        )
        assignment_id = self.kwargs.get("assignment_id")
        assignment = AssignmentRequest.objects.get(id=assignment_id)
        serializer.save(author=author, studygroup=studygroup, assignment=assignment)

    @extend_schema(summary="스터디그룹 과제 제출을 상세 조회합니다.", deprecated=True)
    def retrieve(self, request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 과제 제출을 수정합니다.", deprecated=True)
    def update(self, request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 과제 제출을 부분 수정합니다.", deprecated=True)
    def partial_update(self, request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary="스터디그룹 과제 제출을 삭제합니다.", deprecated=True)
    def destroy(self, request, *args, **kwargs) -> Response:
        return super().destroy(request, *args, **kwargs)
