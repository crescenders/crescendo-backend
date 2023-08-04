from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts import views

urlpatterns = [
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/google/", views.GoogleLogin.as_view(), name="google_login"),
    path("login/kakao/", views.KakaoLogin.as_view(), name="kakao_login"),
    path("signup/", include("allauth.urls"), name="socialaccount_signup"),
]
