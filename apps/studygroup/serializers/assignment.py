from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.serializers import ProfileSerializer
from apps.studygroup.models import AssignmentRequest, AssignmentSubmission


class AssignmentReadSerializer(serializers.ModelSerializer[AssignmentRequest]):
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


class AssignmentCreateSerializer(serializers.ModelSerializer[AssignmentRequest]):
    """
    스터디그룹의 과제를 생성하기 위한 serializer 입니다.
    """

    class Meta:
        model = AssignmentRequest
        fields = [
            "title",
            "content",
        ]


class AssignmentSubmissionListReadSerializer(
    serializers.ModelSerializer[AssignmentRequest]
):
    """
    멤버들이 제출한 과제의 목록을 조회하기 위한 serializer 입니다.
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


class AssignmentSubmissionDetailReadSerializer(AssignmentSubmissionListReadSerializer):
    """
    멤버들이 제출한 과제의 상세정보를 조회하기 위한 serializer 입니다.
    """

    class Meta:
        model = AssignmentSubmission
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
        ]


class AssignmentSubmissionCreateSerializer(
    serializers.ModelSerializer[AssignmentRequest]
):
    """
    새로운 과제를 제출하기 위한 serializer 입니다.
    """

    class Meta:
        model = AssignmentSubmission
        fields = [
            "title",
            "content",
        ]

    def validate(self, attrs: dict) -> dict:
        """
        1. 하나의 과제에 대해 한 명의 유저가 여러 번 제출하는 것을 방지합니다.
        2. 스터디그룹의 활동일이 시작되기 전, 과제를 제출하는 것을 방지합니다.
        """
        studygroup_uuid = self.context["view"].kwargs["studygroup_uuid"]
        assignment_id = self.context["view"].kwargs["assignment_id"]
        request_user = self.context["request"].user

        if AssignmentSubmission.objects.filter(
            studygroup__uuid=studygroup_uuid,
            assignment_id=assignment_id,
            author__user=request_user,
        ).exists():
            raise serializers.ValidationError(
                _("You have already submitted this assignment.")
            )

        if not AssignmentRequest.objects.filter(
            studygroup__uuid=studygroup_uuid,
            id=assignment_id,
            studygroup__start_date__lte=timezone.now(),
        ).exists():
            raise serializers.ValidationError(
                _("You cannot submit an assignment before the activity starts.")
            )

        return attrs


class AssignmentSubmissionUpdateSerializer(
    serializers.ModelSerializer[AssignmentRequest]
):
    """
    과제 제출을 수정하기 위한 serializer 입니다.
    """

    class Meta:
        model = AssignmentSubmission
        fields = [
            "title",
            "content",
        ]


class AssignmentSubmissionDeleteSerializer(
    serializers.ModelSerializer[AssignmentRequest]
):
    """
    과제 제출을 삭제하기 위한 serializer 입니다.
    """

    class Meta:
        model = AssignmentSubmission
        fields = [
            "title",
            "content",
        ]
