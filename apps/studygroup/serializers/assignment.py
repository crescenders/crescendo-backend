from collections import OrderedDict
from typing import Any

from rest_framework import serializers

from apps.accounts.serializers import ProfileSerializer
from apps.studygroup.models import (
    AssignmentRequest,
    AssignmentSubmission,
    StudyGroup,
    StudyGroupMember,
)


class StudyGroupAssignmentReadSerializer(
    serializers.ModelSerializer[AssignmentRequest]
):
    """
    스터디그룹의 과제를 조회하기 위한 serializer 입니다.
    """

    author = ProfileSerializer(
        source="author.user",
        read_only=True,
    )

    class Meta:
        model = AssignmentRequest
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
        ]


class StudyGroupAssignmentCreateSerializer(
    serializers.ModelSerializer[AssignmentRequest]
):
    """
    스터디그룹의 과제를 생성하기 위한 serializer 입니다.
    """

    class Meta:
        model = AssignmentRequest
        fields = [
            "title",
            "content",
        ]


class StudyGroupAssignmentSubmissionReadSerializer(
    serializers.ModelSerializer[AssignmentRequest]
):
    """
    스터디그룹의 과제 제출 목록을 조회하기 위한 serializer 입니다.
    """

    author = ProfileSerializer(
        source="author.user",
        read_only=True,
    )

    class Meta:
        model = AssignmentSubmission
        fields = [
            "id",
            "author",
            "title",
            "created_at",
            "updated_at",
        ]


class StudyGroupAssignmentSubmissionCreateSerializer(
    serializers.ModelSerializer[AssignmentRequest]
):
    """
    스터디그룹의 과제 제출을 생성하기 위한 serializer 입니다.
    """

    class Meta:
        model = AssignmentSubmission
        fields = [
            "title",
            "content",
        ]

    def validate(self, attrs: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        """
        이미 과제를 제출한 상태인지 확인합니다.
        """
        uuid = self.__dict__["_context"]["view"].kwargs["studygroup_uuid"]
        studygroup = StudyGroup.objects.get(uuid=uuid)
        assignment_id = self.__dict__["_context"]["view"].kwargs["assignment_id"]
        assignment = AssignmentRequest.objects.get(id=assignment_id)
        request_user = self.__dict__["_context"]["request"].user
        request_member = StudyGroupMember.objects.get(
            studygroup=studygroup, user=request_user
        )
        if AssignmentSubmission.objects.filter(
            studygroup=studygroup, assignment=assignment, author=request_member
        ).exists():
            raise serializers.ValidationError(
                "You have already submitted this assignment."
            )
        return attrs
