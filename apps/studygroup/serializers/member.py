from collections import OrderedDict
from typing import Any

from rest_framework import serializers

from apps.accounts.serializers import ProfileSerializer
from apps.studygroup.models import StudyGroup, StudyGroupMember, StudyGroupMemberRequest


class LeaderReadSerializer(serializers.ModelSerializer[StudyGroupMember]):
    uuid = serializers.UUIDField(source="user.uuid")
    email = serializers.EmailField(source="user.email")
    username = serializers.CharField(source="user.username")

    class Meta:
        model = StudyGroupMember
        fields = [
            "uuid",
            "email",
            "username",
        ]


class StudyGroupMemberReadSerializer(serializers.ModelSerializer[StudyGroupMember]):
    """
    스터디그룹의 멤버를 조회하기 위한 serializer 입니다.
    """

    user = ProfileSerializer(
        read_only=True,
    )

    class Meta:
        model = StudyGroupMember
        fields = [
            "id",
            "user",
            "is_leader",
            "created_at",
        ]


class StudyGroupMemberRequestCreateSerializer(
    serializers.ModelSerializer[StudyGroupMemberRequest]
):
    """
    스터디그룹 가입 요청을 생성하기 위한 serializer 입니다.
    """

    class Meta:
        model = StudyGroupMemberRequest
        fields = [
            "request_message",
        ]

    def validate(self, attrs: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        """
        1. 스터디그룹의 모집이 마감되었는지 확인합니다.
        2. 이미 스터디그룹에 가입되어 있는지 확인합니다.
        3. 이미 스터디그룹 가입 요청을 보냈는지 확인합니다.
        """
        uuid = self.__dict__["_context"]["view"].kwargs["studygroup_uuid"]
        studygroup = StudyGroup.objects.get(uuid=uuid)
        if studygroup.is_closed:
            raise serializers.ValidationError(
                "The studygroup is already closed. You can't join it."
            )
        members = [member.user for member in studygroup.members.all()]
        request_user = self.__dict__["_context"]["request"].user
        if request_user in members:
            raise serializers.ValidationError(
                "You are already a member of this studygroup."
            )
        if StudyGroupMemberRequest.objects.filter(
            studygroup=studygroup, user=request_user
        ).exists():
            raise serializers.ValidationError(
                "You have already sent a request to join this studygroup."
            )
        return attrs


class StudyGroupMemberRequestReadSerializer(
    serializers.ModelSerializer[StudyGroupMemberRequest]
):
    """
    스터디그룹 가입 요청을 조회하기 위한 serializer 입니다.
    """

    user = ProfileSerializer(
        read_only=True,
    )

    class Meta:
        model = StudyGroupMemberRequest
        fields = [
            "id",
            "user",
            "request_message",
        ]


class StudyGroupMemberRequestManageSerializer(
    serializers.ModelSerializer[StudyGroupMemberRequest]
):
    """
    스터디그룹 가입 요청을 승인하거나 거절하기 위한 serializer 입니다.
    """

    class Meta:
        model = StudyGroupMemberRequest
        fields = []
