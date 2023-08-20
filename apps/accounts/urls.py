from django.urls import include, path

from apps.accounts import views

urlpatterns = [
    # 회원가입
    path("signup/", include("allauth.urls"), name="socialaccount_signup"),
    # 로그인
    path("login/refresh/", views.TokenRefreshAPI.as_view(), name="token_refresh"),
    path("login/google/", views.GoogleLoginAPI.as_view(), name="google_login"),
    path("login/kakao/", views.KakaoLoginAPI.as_view(), name="kakao_login"),
    # 내 정보 조회/수정/탈퇴
    path("profiles/me/", views.ProfileAPI.as_view(), name="user_profile"),
]
