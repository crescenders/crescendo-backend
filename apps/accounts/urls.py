from dataclasses import dataclass

from django.urls import include, path

from apps.accounts.views import (
    GoogleLoginAPI,
    LogoutAPI,
    MyProfileAPI,
    MyStudyAPI,
    TokenRefreshAPI,
    UUIDProfileAPI,
)


@dataclass(frozen=True)
class AccountsURLs:
    SIGNUP: str = "signup"
    REFRESH_LOGIN: str = "refresh-login"
    GOOGLE_LOGIN: str = "google-login"
    LOGOUT: str = "token-blacklist"
    MY_PROFILE: str = "profile-login-user"
    MY_PROFILE_STUDIES: str = "profile-login-studies"
    UUID_PROFILE: str = "profile-uuid"


urlpatterns = [
    # 회원가입
    path(
        "signup/",
        include("allauth.urls"),
        name="socialaccount-signup",
    ),
    # 로그인
    path(
        "login/",
        include(
            [
                path(
                    "refresh/",
                    TokenRefreshAPI.as_view(),
                    name="refresh-login",
                ),
                path(
                    "google/",
                    GoogleLoginAPI.as_view(),
                    name="google-login",
                ),
            ]
        ),
    ),
    # 로그아웃
    path(
        "logout/",
        LogoutAPI.as_view(),
        name="token-blacklist",
    ),
    # 프로필
    path(
        "profiles/",
        include(
            [
                path(
                    "me/",
                    MyProfileAPI.as_view(),
                    name="profile-login-user",
                ),
                path(
                    "me/studies/",
                    MyStudyAPI.as_view(),
                    name="profile-login-studies",
                ),
                path(
                    "<uuid:user_uuid>/",
                    UUIDProfileAPI.as_view(),
                    name="profile-uuid",
                ),
            ]
        ),
    ),
]
