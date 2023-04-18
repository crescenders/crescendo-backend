from marshmallow import fields


class PaginationResultSchemaMixin:
    count = fields.Integer(metadata={"description": "전체 아이템 개수"})
    next_num = fields.URL(metadata={"description": "다음 페이지 URL"})
    previous_num = fields.URL(metadata={"description": "이전 페이지 URL"})
