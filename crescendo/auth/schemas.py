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
    pass


class UserSchema(Schema):
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
    results = fields.List(fields.Nested(UserSchema), metadata={"description": "사용자 목록"})
