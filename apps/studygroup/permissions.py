from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.studygroup.models import StudyGroup, StudyGroupMember


class IsLeaderOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
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


class StudyGroupAddMember(permissions.BasePermission):
    """
    스터디그룹에 멤버를 추가할 수 있는 권한을 설정합니다.
    - 스터디그룹의 리더만 가능
    """

    def has_object_permission(
        self, request: Request, view: APIView, obj: StudyGroupMember
    ) -> bool:
        return request.user in [member.user for member in obj.study_group.leaders.all()]
