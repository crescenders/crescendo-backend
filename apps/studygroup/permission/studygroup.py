from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.studygroup.models import StudyGroup


def _get_studygroup(view: APIView) -> StudyGroup:
    assert view.kwargs.get("studygroup_uuid") is not None, _(
        f"{view.__class__.__name__} requires studygroup_uuid argument in view"
    )
    studygroup_uuid = view.kwargs.get("studygroup_uuid")
    return get_object_or_404(StudyGroup, uuid=studygroup_uuid)


class IsStudygroupMember(permissions.BasePermission):
    """
    스터디그룹의 멤버인지 확인합니다.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        studygroup = _get_studygroup(view)
        return studygroup.members.filter(user=request.user).exists()


class IsStudygroupMemberOrReadOnly(permissions.BasePermission):
    """
    스터디그룹의 멤버이거나, GET, HEAD, OPTIONS 요청인지 확인합니다.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        studygroup = _get_studygroup(view)
        return (
            studygroup.members.filter(user=request.user).exists()
            or request.method in permissions.SAFE_METHODS
        )


class IsStudygroupLeader(permissions.BasePermission):
    """
    스터디그룹의 리더인지 확인합니다.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        studygroup = _get_studygroup(view)
        return (
            request.user.is_authenticated
            and studygroup.leaders.filter(user=request.user).exists()
        )
