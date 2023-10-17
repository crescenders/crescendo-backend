from django.urls import path

from apps.studygroup.views.category import CategoryListAPI
from apps.studygroup.views.members import (
    StudyGroupMemberDetailAPI,
    StudyGroupMemberListAPI,
    StudyGroupMemberRequestDetailAPI,
    StudyGroupMemberRequestListAPI,
)
from apps.studygroup.views.studygroup import StudyGroupAPISet

urlpatterns = [
    path(
        "studies/",
        StudyGroupAPISet.as_view({"get": "list", "post": "create"}),
        name="studygroup_list",
    ),
    path(
        "studies/<uuid:uuid>/",
        StudyGroupAPISet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="studygroup_detail",
    ),
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
