from typing import List
from flask_restx import fields, Api


class UserDTO:
    def __init__(self, api: Api):
        self.api = api
        self.all_fields = {
            "id": fields.Integer(
                example="1",
                readonly=True,
                description="사용자 ID",
            ),
            "uuid": fields.String(
                example="244163bd-ad03-4f87-b936-bd8094c48bce",
                readonly=True,
                description="사용자 UUID",
            ),
            "email": fields.String(
                example="chulsu38@gmail.com", required=True, description="사용자 이메일"
            ),
            "username": fields.String(
                example="chulsu38",
                required=True,
                description="사용자 닉네임",
            ),
            "first_name": fields.String(
                example="Chul",
                required=True,
                description="사용자 이름",
            ),
            "last_name": fields.String(
                example="Su",
                required=True,
                description="사용자 성",
            ),
            "gender": fields.String(
                example="남자",
                required=True,
                description="사용자 성별",
            ),
            "phone_number": fields.String(
                example="010-1234-5678",
                required=True,
                description="사용자 전화번호",
            ),
            "password": fields.String(
                example="password",
                required=True,
                description="사용자 비밀번호",
            ),
        }

    def get_model(self, name: str, selected_fields: List[str]) -> fields.Raw:
        model_dict = {
            field_name: self.all_fields[field_name]
            for field_name in set(selected_fields) & set(self.all_fields)
        }
        return self.api.model(name, model_dict)
