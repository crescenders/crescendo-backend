from marshmallow import Schema, fields

from core.schemas import fields as fullask_fields
from core.schemas.pagination import PaginationResultSchema


class UserSchema(Schema):
    """사용자 한 명에 대한 직렬화 규칙을 정의합니다."""

    uuid = fields.UUID(
        dump_only=True,
        metadata={"description": "사용자 UUID"},
    )
    username = fields.String(
        metadata={"description": "사용자 닉네임"},
    )
    email = fields.Email(
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


class UserFilteringArgsSchema(Schema):
    """사용자 목록 조회 시, 필터링 쿼리스트링을 정의합니다."""

    username = fields.String(
        metadata={"description": "닉네임에 해당 문자열이 포함된 모든 사용자를 찾습니다."},
    )
    email = fields.String(
        metadata={"description": "이메일에 해당 문자열이 포함된 모든 사용자를 찾습니다."},
    )


class SortingArgsSchema(Schema):
    """사용자 목록 조회 시, 정렬 쿼리스트링을 정의합니다."""

    sorting = fields.List(
        fullask_fields.SortDict(),
        metadata={"description": "정렬 조건, `찾고자 하는 필드명:(desc 혹은 asc)` 의 형식을 준수해야 합니다."},
    )


class UserListSchema(PaginationResultSchema):
    """사용자 목록에 대한 직렬화 규칙을 정의합니다."""

    results = fields.List(
        fields.Nested(UserSchema()), metadata={"description": "사용자 목록"}
    )


class GoogleOauthArgsSchema(Schema):
    google_jwt = fields.String()
