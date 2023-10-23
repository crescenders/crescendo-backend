from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.studygroup.views.assignments import StudyGroupAssignmentRequestAPISet
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
    basename="assignment",
)

urlpatterns = [
    path("", include(studygroup_router.urls)),
    path("studies/<uuid:uuid>/", include(assignment_router.urls)),
    path(
        "studies/<uuid:uuid>/members/",
        StudyGroupMemberListAPI.as_view(),
        name="studygroupmember-list",
    ),
    path(
        "studies/<uuid:uuid>/members/<int:pk>/",
        StudyGroupMemberDetailAPI.as_view(),
        name="studygroupmember-detail",
    ),
    path(
        "studies/<uuid:uuid>/requests/",
        StudyGroupMemberRequestListAPI.as_view(),
        name="studygroupmember-request-list",
    ),
    path(
        "studies/<uuid:uuid>/requests/<int:pk>/",
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
