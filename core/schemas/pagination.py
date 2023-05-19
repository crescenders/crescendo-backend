from marshmallow import Schema, fields, post_load
from marshmallow.validate import Range

from core.entities.pagination import PaginationRequest, PaginationResponse


class PaginationRequestSchema(Schema):
    page = fields.Integer(
        validate=Range(min=1),
        metadata={"description": "조회하고자 하는 페이지 번호입니다."},
    )
    per_page = fields.Integer(
        validate=Range(min=1),
        metadata={"description": "한 페이지의 아이템 개수입니다."},
    )

    @post_load
    def to_entity(self, data, **kwargs) -> PaginationRequest:
        return PaginationRequest(**data)


class PaginationResponseSchema(Schema):
    count = fields.Integer(metadata={"description": "전체 아이템 개수"})
    next_page = fields.Integer(metadata={"description": "다음 페이지 숫자"})
    previous_page = fields.Integer(metadata={"description": "이전 페이지 숫자"})

    @post_load
    def to_entity(self, data, **kwargs) -> PaginationResponse:
        return PaginationResponse(**data)
