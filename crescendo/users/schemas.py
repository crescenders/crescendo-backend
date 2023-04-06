from marshmallow import Schema, fields, validate


class ArgsSchema(Schema):
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(load_default=10)
    filter_by = fields.String(load_default=None)
    ordering = fields.String(
        load_validate=validate.OneOf(["asc", "desc"]), load_default="desc"
    )


class UserSchema(Schema):
    id = fields.Integer(
        dump_only=True,
        metadata={
            "description": "사용자 ID",
            "example": 1,
        },
    )
    uuid = fields.String()
    username = fields.String()
    email = fields.String()
