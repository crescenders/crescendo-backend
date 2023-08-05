from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Django 기본 관리자 페이지
    path(
        "admin/",
        admin.site.urls,
        name="admin",
    ),
    # Django REST Framework 로그인/로그아웃
    path(
        "api-auth/",
        include("rest_framework.urls"),
        name="rest_framework",
    ),
    # API 문서
    path(
        "docs/json",
        SpectacularJSONAPIView.as_view(),
        name="schema-json",
    ),
    path(
        "docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema-json"),
        name="swagger",
    ),
    path(
        "docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema-json"),
        name="redoc",
    ),
    # Local Apps
    path(
        "api/v1/auth/",
        include("accounts.urls"),
        name="accounts",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
