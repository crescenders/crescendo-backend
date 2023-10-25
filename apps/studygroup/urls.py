from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.studygroup.views.assignments import (
    StudyGroupAssignmentRequestAPISet,
    StudyGroupAssignmentSubmissionAPISet,
)
from apps.studygroup.views.category import CategoryListAPI
from apps.studygroup.views.members import (
    StudyGroupMemberDetailAPI,
    StudyGroupMemberListAPI,
    StudyGroupMemberRequestDetailAPI,
    StudyGroupMemberRequestListAPI,
)
from apps.studygroup.views.studygroup import StudyGroupAPISet
from apps.studygroup.views.tags import TagRandomListAPI

studygroup_router = SimpleRouter()
studygroup_router.register("studies", StudyGroupAPISet, basename="studygroup")

assignment_router = SimpleRouter()
assignment_router.register(
    r"assignments",
    StudyGroupAssignmentRequestAPISet,
    basename="assignment-request",
)

assignment_submission_router = SimpleRouter()
assignment_submission_router.register(
    r"submissions",
    StudyGroupAssignmentSubmissionAPISet,
    basename="assignment-submission",
)

urlpatterns = [
    path("", include(studygroup_router.urls)),
    path("studies/<uuid:studygroup_uuid>/", include(assignment_router.urls)),
    path(
        "studies/<uuid:studygroup_uuid>/assignments/<int:assignment_id>/",
        include(assignment_submission_router.urls),
    ),
    path(
        "studies/<uuid:studygroup_uuid>/members/",
        StudyGroupMemberListAPI.as_view(),
        name="studygroupmember-list",
    ),
    path(
        "studies/<uuid:studygroup_uuid>/members/<int:pk>/",
        StudyGroupMemberDetailAPI.as_view(),
        name="studygroupmember-detail",
    ),
    path(
        "studies/<uuid:studygroup_uuid>/requests/",
        StudyGroupMemberRequestListAPI.as_view(),
        name="studygroupmember-request-list",
    ),
    path(
        "studies/<uuid:studygroup_uuid>/requests/<int:pk>/",
        StudyGroupMemberRequestDetailAPI.as_view(),
        name="studygroupmember-request-detail",
    ),
    path(
        "categories/",
        CategoryListAPI.as_view(),
        name="category-list",
    ),
    path(
        "tags/",
        TagRandomListAPI.as_view(),
        name="tag-list",
    ),
]
