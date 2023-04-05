from flask_restx import fields

from crescendo.users import users_api

user = users_api.model(
    name="User",
    model=dict(
        id=fields.Integer(
            readonly=True,
            example="1",
            description="사용자의 데이터베이스 id",
        ),
        uuid=fields.String(
            required=True,
            example="99cd6b7a-4b22-440a-8671-0c572d06926",
            description="사용자의 데이터베이스 uuid",
        ),
        email=fields.String(
            required=True,
            example="example@example.com",
            description="사용자 계정 이메일",
        ),
        username=fields.String(
            required=True,
            example="goddessana",
            description="사용자 닉네임",
        ),
    ),
)

user_list = users_api.model(
    name="UserList",
    model=dict(
        total_user_count=fields.Integer(
            readonly=True,
            example="1",
            description="전체 사용자 수",
        ),
        current_page=fields.Integer(
            readonly=True,
            example="2",
            description="현재 페이지",
        ),
        total_page=fields.Integer(
            readonly=True,
            example="15",
            description="전체 페이지 수",
        ),
        has_next=fields.Boolean(
            readonly=True,
            example=True,
            description="다음 페이지 존재 여부",
        ),
        has_prev=fields.Boolean(
            readonly=True,
            example=False,
            description="이전 페이지 존재 여부",
        ),
        users=fields.List(
            fields.Nested(user),
        ),
    ),
)
