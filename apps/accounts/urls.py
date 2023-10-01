from django.urls import include, path

from apps.accounts import views

urlpatterns = [
    # 회원가입
    path("signup/", include("allauth.urls"), name="socialaccount_signup"),
    # 로그인
    path("login/refresh/", views.TokenRefreshAPI.as_view(), name="token_refresh"),
    path("login/google/", views.GoogleLoginAPI.as_view(), name="google_login"),
    # 로그아웃
    path("logout/", views.LogoutAPI.as_view(), name="token_blacklist"),
    # 내 정보 조회/수정/탈퇴
    path("profiles/me/", views.MyProfileAPI.as_view(), name="user_profile_me"),
    path("profiles/me/studies/", views.MyStudyAPI.as_view(), name="user_study_me"),
    # UUID 기반 유저 정보 조회
    path(
        "profiles/<uuid:uuid>/",
        views.UUIDProfileAPI.as_view(),
        name="user_profile_uuid",
    ),
]
