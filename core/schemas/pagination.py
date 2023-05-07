from marshmallow import Schema, fields
from marshmallow.validate import Range


class PaginationRequestSchema(Schema):
    page = fields.Integer(
        validate=Range(min=1),
        metadata={"description": "조회하고자 하는 페이지 번호입니다."},
    )
    per_page = fields.Integer(
        validate=Range(min=1),
        metadata={"description": "한 페이지의 아이템 개수입니다."},
    )


class PaginationResponseSchema(Schema):
    count = fields.Integer(metadata={"description": "전체 아이템 개수"})
    next_page = fields.URL(metadata={"description": "다음 페이지 URL"})
    previous_page = fields.URL(metadata={"description": "이전 페이지 URL"})
