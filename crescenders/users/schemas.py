from enum import Enum

from flask_restx import Model
from flask_restx import fields as restx_fields
from marshmallow import Schema
from marshmallow import fields as marshmallow_fields


class UserSchema(Schema):
    id = marshmallow_fields.Integer()
    uuid = marshmallow_fields.UUID()
    email = marshmallow_fields.Email()
    username = marshmallow_fields.String()
    first_name = marshmallow_fields.String()
    last_name = marshmallow_fields.String()
    gender = marshmallow_fields.Enum(
        enum=Enum("Gender", {"MALE": "남자", "FEMALE": "여자"})
    )
    phone_number = marshmallow_fields.String()
    password = marshmallow_fields.String()
    created_at = marshmallow_fields.DateTime()
    updated_at = marshmallow_fields.DateTime()


class UserRestXModel(Model):
    id = restx_fields.String("id", description="아이디", example="user_id", required=True)
