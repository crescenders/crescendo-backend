from flask_restx import Namespace

users_api = Namespace(
    "Users",
    description="사용자 리소스를 다루는 API입니다.",
)
