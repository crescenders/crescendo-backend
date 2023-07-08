from fullask_rest_framework.schemas import BaseFilteringSchema, PaginationResponseSchema
from marshmallow import Schema, fields


class UserSchema(Schema):
    uuid = fields.UUID(
        dump_only=True,
        metadata={"description": "사용자 UUID"},
    )
    username = fields.String(
        required=True,
        metadata={"description": "사용자 닉네임"},
    )
    email = fields.Email(
        dump_only=True,
        metadata={"description": "사용자 이메일"},
    )
    created_at = fields.DateTime(
        dump_only=True,
        metadata={"description": "사용자 가입일자"},
    )
    updated_at = fields.DateTime(
        dump_only=True,
        metadata={"description": "사용자 정보 수정일자"},
    )


class PaginatedUserListSchema(PaginationResponseSchema):
    results = fields.List(
        fields.Nested(UserSchema()), metadata={"description": "사용자 목록"}
    )


class UserFilteringArgsSchema(BaseFilteringSchema):
    username = fields.String(
        metadata={"description": "닉네임에 해당 문자열이 포함된 모든 사용자를 찾습니다."},
    )
    email = fields.String(
        metadata={"description": "이메일에 해당 문자열이 포함된 모든 사용자를 찾습니다."},
    )


class GoogleOauthArgsSchema(Schema):
    google_jwt = fields.String()


class JWTSchema(Schema):
    access_token = fields.String()
    refresh_token = fields.String()
