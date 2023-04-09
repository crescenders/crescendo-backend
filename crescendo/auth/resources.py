from flask.views import MethodView

from crescendo.auth import auth_api


@auth_api.route("/google-login/")
class GoogleLoginAPI(MethodView):
    """Google 소셜 로그인을 진행합니다."""

    def post(self):
        return None


@auth_api.route("/kakao-login/")
class KakaoLoginAPI(MethodView):
    """Kakao 소셜 로그인을 진행합니다."""

    def post(self):
        return None
