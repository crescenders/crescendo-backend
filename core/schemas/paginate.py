from marshmallow import Schema, fields


class PaginateSchema(Schema):
    page = fields.Integer(required=False, description="페이지의 숫자")
    per_page = fields.Integer(required=False, description="페이지당 개수")
