from flask_restx import Resource

from crescendo.auth import auth_api


@auth_api.route("/")
class UserListAPI(Resource):
    def post(self):
        """사용자 한 명을 생성합니다.
        비밀번호를 암호화하여 저장합니다."""
        return None

    def post(self):
        """사용자 한 명을 생성합니다.
        비밀번호를 암호화하여 저장합니다."""
        return None
