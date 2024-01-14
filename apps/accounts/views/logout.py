from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenBlacklistView as _TokenBlacklistView


@extend_schema(
    tags=["로그인/로그아웃 API"],
    summary="로그아웃합니다. refresh token 을 blacklist 에 추가합니다.",
)
class LogoutAPI(_TokenBlacklistView):  # type: ignore
    """
    로그아웃에 사용된 refresh token 은 더 이상 사용될 수 없습니다.
    """

    pass
