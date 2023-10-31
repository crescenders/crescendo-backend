from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.studygroup.models import AssignmentSubmission


def _get_assignment(view: APIView) -> AssignmentSubmission:
    assert view.kwargs.get("assignment_id") is not None, _(
        f"{view.__class__.__name__} requires assignment_id argument in view"
    )
    assignment_id = view.kwargs.get("assignment_id")
    return get_object_or_404(AssignmentSubmission, id=assignment_id)


class IsAssignmentSubmissionAuthor(permissions.BasePermission):
    """
    현재 요청을 보낸 유저가 과제의 작성자인지 확인합니다.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        assignment = _get_assignment(view)
        return assignment.author.user == request.user


class IsAssignmentSubmissionAuthorOrReadOnly(permissions.BasePermission):
    """
    현재 요청을 보낸 유저가 과제의 작성자이거나, GET, HEAD, OPTIONS 요청인지 확인합니다.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        assignment = _get_assignment(view)
        return (
            assignment.author.user == request.user
            or request.method in permissions.SAFE_METHODS
        )
