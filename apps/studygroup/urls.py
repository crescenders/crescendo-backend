from django.urls import path

from apps.studygroup import views

urlpatterns = [
    path(
        "studies/",
        views.StudyGroupAPISet.as_view({"get": "list", "post": "create"}),
        name="studygroup_list",
    ),
    path(
        "studies/<uuid:uuid>/",
        views.StudyGroupAPISet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="studygroup_detail",
    ),
    path(
        "categories/",
        views.CategoryListAPI.as_view(),
        name="category_list",
    ),
]
