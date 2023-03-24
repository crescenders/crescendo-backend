from marshmallow import Schema, fields


class PaginateSchema(Schema):
    page = fields.Integer(default=1)
    per_page = fields.Integer(default=10)
    total = fields.Integer(dump_only=True)
