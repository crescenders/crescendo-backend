from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from apps.studygroup.models import (
    StudyGroup,
    StudyGroupAssignmentRequest,
    StudyGroupMember,
)


class StudyGroupCreatePermission(permissions.IsAuthenticated):
    """
    스터디그룹을 생성할 수 있는 권한을 설정합니다.
    """


class StudyGroupDeleteOrUpdatePermission(permissions.BasePermission):
    """
    스터디그룹을 삭제하거나 수정할 수 있는 권한을 설정합니다.
    - 스터디그룹의 리더만 가능
    """

    def has_object_permission(
        self, request: Request, view: APIView, obj: StudyGroup
    ) -> bool:
        group_leaders = [leader.user for leader in obj.leaders]
        return request.user in group_leaders


class IsLeaderOrReadOnly(permissions.BasePermission):
    """
    스터디그룹에 대한 권한을 설정합니다.
    - 목록 보기, 상세 보기: 누구나 가능
    - 생성: 로그인한 사람만 가능
    - 수정, 삭제: 스터디그룹장만 가능
    """

    def has_object_permission(
        self, request: Request, view: APIView, obj: StudyGroup
    ) -> bool:
        group_leaders = [leader.user for leader in obj.leaders]
        return (
            request.method in permissions.SAFE_METHODS or request.user in group_leaders
        )


class IsLeaderOrReadOnlyForAssignment(permissions.BasePermission):
    """
    스터디그룹에 과제에 대한 권한을 설정합니다.
    - 목록 조회: 누구나 가능
    - 상세 조회: 멤버만 가능
    - 생성: 스터디그룹장만 가능
    - 수정, 삭제: 스터디그룹장만 가능
    """

    def has_permission(self, request: Request, view: ViewSet) -> bool:
        if view.action == "retrieve":
            return request.user in [
                member.user
                for member in StudyGroup.objects.get(
                    uuid=view.kwargs["uuid"]
                ).members.all()
            ]
        if (
            view.action == "create"
            or view.action == "update"
            or view.action == "destroy"
        ):
            return request.user in [
                leader.user
                for leader in StudyGroup.objects.get(
                    uuid=view.kwargs["uuid"]
                ).leaders.all()
            ]
        return True

    def has_object_permission(
        self, request: Request, view: APIView, obj: StudyGroupAssignmentRequest
    ) -> bool:
        return request.user in [leader.user for leader in obj.studygroup.leaders.all()]


class IsStudyGroupMember(permissions.BasePermission):
    """
    스터디그룹의 멤버인지 확인하는 권한을 설정합니다.
    - 스터디그룹의 멤버만 가능
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        studygroup = StudyGroup.objects.get(uuid=view.kwargs["uuid"])
        return request.user in [member.user for member in studygroup.members.all()]


class IsStudyGroupLeader(permissions.BasePermission):
    """
    스터디그룹의 멤버 신청자를 조회할 수 있는 권한을 설정합니다.
    - 스터디그룹의 리더만 가능
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        studygroup = StudyGroup.objects.get(uuid=view.kwargs["uuid"])
        return request.user in [leader.user for leader in studygroup.leaders.all()]


class StudyGroupMemberRead(permissions.BasePermission):
    """
    스터디그룹의 멤버를 조회할 수 있는 권한을 설정합니다.
    - 스터디그룹에 참여하고 있는 멤버만 가능
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        studygroup = StudyGroup.objects.get(uuid=view.kwargs["uuid"])
        return request.user in [member.user for member in studygroup.members.all()]


class StudyGroupAddMember(permissions.BasePermission):
    """
    스터디그룹에 멤버를 추가할 수 있는 권한을 설정합니다.
    - 스터디그룹의 리더만 가능
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        """
        "현재 스터디그룹에 가입되어 있는 멤버를 조회" 하고자 하는 경우, 로그인한 유저는 스터디그룹의 멤버이거나 리더이어야 합니다.
        """
        studygroup = StudyGroup.objects.get(uuid=view.kwargs["uuid"])
        if request.query_params.get("is_approved") == "true":
            return request.user in [member.user for member in studygroup.members.all()]
        return request.user in [
            member.user
            for member in StudyGroup.objects.get(uuid=view.kwargs["uuid"]).leaders.all()
        ]

    def has_object_permission(
        self, request: Request, view: APIView, obj: StudyGroupMember
    ) -> bool:
        return request.user in [member.user for member in obj.studygroup.leaders.all()]
