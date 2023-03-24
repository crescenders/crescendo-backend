from typing import List

from flask_restx import Api, Model
from flask_restx import fields as restx_fields


class UserDTO(Model):
    id = restx_fields.Integer(example="1", readonly=True, description="사용자 ID")
    uuid = restx_fields.String(
        example="244163bd-ad03-4f87-b936-bd8094c48bce",
        readonly=True,
        description="사용자 UUID",
    )
    email = restx_fields.String(
        example="chulsu38@gmail.com", required=True, description="사용자 이메일"
    )
    username = restx_fields.String(
        example="chulsu38", required=True, description="사용자 닉네임"
    )
    first_name = restx_fields.String(
        example="Chul", required=True, description="사용자 이름"
    )
    last_name = restx_fields.String()


class UserMarshaller:
    def __init__(self, api: Api):
        self.api = api
        self.all_fields = {
            "id": restx_fields.Integer(
                example="1", readonly=True, description="사용자 ID"
            ),
            "uuid": restx_fields.String(
                example="244163bd-ad03-4f87-b936-bd8094c48bce",
                readonly=True,
                description="사용자 UUID",
            ),
            "email": restx_fields.String(
                example="chulsu38@gmail.com", required=True, description="사용자 이메일"
            ),
            "username": restx_fields.String(
                example="chulsu38", required=True, description="사용자 닉네임"
            ),
            "first_name": restx_fields.String(
                example="Chul", required=True, description="사용자 이름"
            ),
            "last_name": restx_fields.String(
                example="Su", required=True, description="사용자 성"
            ),
            "gender": restx_fields.String(
                example="남자", required=True, enum=["남자", "여자"], description="사용자 성별"
            ),
            "phone_number": restx_fields.String(
                example="010-1234-5678", required=True, description="사용자 전화번호"
            ),
            "password": restx_fields.String(
                example="password", required=True, description="사용자 비밀번호"
            ),
        }

    def get_restx_model(
        self, name: str, selected_fields: List[str]
    ) -> restx_fields.Raw:
        model_dict = {
            field_name: self.all_fields[field_name]
            for field_name in set(selected_fields) & set(self.all_fields)
        }
        return self.api.model(name, model_dict)
