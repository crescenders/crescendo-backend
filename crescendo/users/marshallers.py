from flask_restx import fields as restx_fields

from core.marshaller.base_marshaller import BaseMarshaller


class BaseUserMarshaller(BaseMarshaller):
    id = restx_fields.String("id", description="id", example="1")
    uuid = restx_fields.String(
        "uuid",
        description="uuid",
        example="6d53e5f9-6ea9-45e2-8e19-3a777dc3feb5",
        format="uuid",
    )
    email = restx_fields.String(
        "email", description="email", example="user@example.com"
    )
    first_name = restx_fields.String(
        "first_name", description="first_name", example="John"
    )
    last_name = restx_fields.String("last_name", description="last_name", example="Doe")
    gender = restx_fields.String("gender", description="gender", example="남자")
    phone_number = restx_fields.String(
        "phone_number", description="phone_number", example="0123456789"
    )
    password = restx_fields.String(
        "password", description="password", example="password"
    )
