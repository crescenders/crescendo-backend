from flask_restx import Namespace

auth_api = Namespace(
    "Auth",
    description="인증 서비스를 다루는 API입니다.",
)
