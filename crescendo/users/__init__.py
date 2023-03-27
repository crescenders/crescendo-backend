from flask_restx import Namespace

user_resource = Namespace(
    "UserResource",
    description="사용자 리소스를 다룹니다.",
)
