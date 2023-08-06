from django.urls import include, path

from accounts import views

urlpatterns = [
    # 회원가입
    path("signup/", include("allauth.urls"), name="socialaccount_signup"),
    # 로그인
    path("login/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path("login/google/", views.GoogleLogin.as_view(), name="google_login"),
    path("login/kakao/", views.KakaoLogin.as_view(), name="kakao_login"),
    # 내 정보 조회/수정/탈퇴
    path("profile/me/", views.ProfileAPI.as_view(), name="user_profile"),
]
