from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)
    description = fields.Str(required=True)


class CategoryCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
