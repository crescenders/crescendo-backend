from django.urls import include, path

from accounts import views

urlpatterns = [
    path("refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path("login/google/", views.GoogleLogin.as_view(), name="google_login"),
    path("login/kakao/", views.KakaoLogin.as_view(), name="kakao_login"),
    path("signup/", include("allauth.urls"), name="socialaccount_signup"),
]
