from apps.accounts.views.login import GoogleLoginAPI
from apps.accounts.views.logout import LogoutAPI
from apps.accounts.views.profile import MyProfileAPI, MyStudyAPI, UUIDProfileAPI
from apps.accounts.views.refresh import TokenRefreshAPI

__all__ = [
    "GoogleLoginAPI",
    "LogoutAPI",
    "MyProfileAPI",
    "MyStudyAPI",
    "UUIDProfileAPI",
    "TokenRefreshAPI",
]
