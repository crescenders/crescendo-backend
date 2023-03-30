from flask_restx import Namespace

users_api = Namespace(
    "UserResource",
    description="사용자 리소스를 다룹니다.",
)
