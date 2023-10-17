from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.studygroup.views.category import CategoryListAPI
from apps.studygroup.views.members import (
    StudyGroupMemberDetailAPI,
    StudyGroupMemberListAPI,
    StudyGroupMemberRequestDetailAPI,
    StudyGroupMemberRequestListAPI,
)
from apps.studygroup.views.studygroup import StudyGroupAPISet

router = DefaultRouter()

router.register("studies", StudyGroupAPISet, basename="studygroup")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "studies/<uuid:uuid>/members/",
        StudyGroupMemberListAPI.as_view(),
        name="studygroup_member_list",
    ),
    path(
        "studies/<uuid:uuid>/members/<int:pk>/",
        StudyGroupMemberDetailAPI.as_view(),
        name="studygroup_member_detail",
    ),
    path(
        "studies/<uuid:uuid>/requests/",
        StudyGroupMemberRequestListAPI.as_view(),
        name="studygroup_member_request_list",
    ),
    path(
        "studies/<uuid:uuid>/requests/<int:pk>/",
        StudyGroupMemberRequestDetailAPI.as_view(),
        name="studygroup_member_request_detail",
    ),
    path(
        "categories/",
        CategoryListAPI.as_view(),
        name="category_list",
    ),
]
