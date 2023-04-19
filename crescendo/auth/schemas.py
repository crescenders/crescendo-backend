from marshmallow import Schema, fields

from core.schemas.request import (
    FilteringArgsSchemaMixin,
    OrderingArgsSchemaMixin,
    PaginateArgsSchemaMixin,
)
from core.schemas.response import PaginationResultSchemaMixin


class UserListArgsSchema(
    PaginateArgsSchemaMixin, FilteringArgsSchemaMixin, OrderingArgsSchemaMixin, Schema
):
    """사용자 목록을 조회하기 위한 여러가지 요청 파라미터입니다."""

    pass


class UserSchema(Schema):
    """사용자 한 명에 대한 직렬화 규칙을 정의합니다."""

    id = fields.Integer(
        dump_only=True,
        metadata={
            "description": "사용자 ID",
            "example": 1,
        },
    )
    uuid = fields.String(
        dump_only=True,
        metadata={
            "description": "사용자 UUID",
            "example": "715fcaff-45f1-4472-814a-a06686241023",
        },
    )
    username = fields.String(
        metadata={
            "description": "사용자 닉네임",
            "example": "goddessana",
        },
    )
    email = fields.String(
        metadata={
            "description": "사용자 이메일",
            "example": "goddessana@gmail.com",
        }
    )


class UserListSchema(PaginationResultSchemaMixin, Schema):
    """사용자 목록에 대한 직렬화 규칙을 정의합니다."""

    results = fields.List(
        fields.Nested(UserSchema()), metadata={"description": "사용자 목록"}
    )


class GoogleOauthArgsSchema(Schema):
    google_jwt = fields.String()
