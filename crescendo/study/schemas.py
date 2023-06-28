from marshmallow import Schema, fields


class CategoryListSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
