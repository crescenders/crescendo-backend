from flask_restx import fields

from crescendo.users import users_api

user = users_api.model(
    "User",
    {
        "id": fields.Integer(
            readonly=True,
            example="1",
            description="사용자의 데이터베이스 id",
        ),
        "uuid": fields.String(
            required=True,
            example="99cd6b7a-4b22-440a-8671-0c572d06926",
            description="사용자의 데이터베이스 uuid",
        ),
        "email": fields.String(
            required=True,
            example="example@example.com",
            description="사용자 계정 이메일",
        ),
        "username": fields.String(
            required=True,
            example="goddessana",
            description="사용자 닉네임",
        ),
    },
)


user_list = users_api.model(
    "UserList",
    {
        "total": fields.Integer(
            readonly=True,
        ),
        "has_next": fields.String(
            readonly=True,
        ),
        "has_prev": fields.String(
            readonly=True,
        ),
        "users": fields.List(
            fields.Nested(user),
        ),
    },
)
