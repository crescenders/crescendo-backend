from core.resources.marshaller.base_marshaller import BaseMarshaller
from core.resources.marshaller.paginate_marshaller import PaginationMarshaller
from flask_restx import fields as restx_fields


class UserMarshaller(BaseMarshaller):
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
    username = restx_fields.String("username", description="username", example="user")
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
    created_at = restx_fields.String(
        "created_at", description="created_at", example="2021-10-10T00:00:00.000Z"
    )
    updated_at = restx_fields.String(
        "updated_at", description="updated_at", example="2021-10-10T00:00:00.000Z"
    )


class UserListMarshaller(PaginationMarshaller):
    pass


class UserDetailMarshaller(PaginationMarshaller):
    pass
