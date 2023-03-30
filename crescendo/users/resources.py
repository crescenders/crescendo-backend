from crescendo.users import users_api
from crescendo.users.marshallers import UserMarshaller
from crescendo.users.services import UserService
from flask import request
from flask_restx import Resource
from flask_restx.reqparse import RequestParser

user_list_marshaller = users_api.model(
    **UserMarshaller().to_model(
        model_name="user_list",
        field_names=[
            "id",
            "uuid",
            "email",
            "username",
            "created_at",
            "updated_at",
        ],
    )
)
user_list_parser = RequestParser().add_argument(
    "email", type=str, required=True, action="store"
)


@users_api.route("/")
class UserList(Resource):
    def __init__(self, service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = service

    @users_api.marshal_list_with(user_list_marshaller)
    @users_api.doc(parser=user_list_parser)
    def get(self):
        """사용자 전체 목록을 조회합니다.
        pagination 혹은 filter 결과가 있을 경우도 처리합니다."""

        return self.user_service.get_all_users()

    def post(self):
        """사용자 한 명을 생성합니다.
        비밀번호를 암호화하여 저장합니다."""

        return self.user_service.create_user(**request.json)


@users_api.route("/<uuid:user_uuid>/")
class UserDetail(Resource):
    def __init__(self, *args, **kwargs):
        self.user_service = UserService()
        super().__init__(*args, **kwargs)

    def get(self, user_uuid):
        """UUID 로 특정되는 사용자 한 명의 정보를 조회합니다."""
        return self.user_service.get_one_user(user_uuid)

    def put(self, user_uuid):
        """UUID로 특정되는 사용자 한 명의 정보를 수정합니다."""
        return self.user_service.update_user(user_uuid, **request.json)

    def delete(self, user_uuid):
        """UUID로 특정되는 사용자 한 명을 삭제합니다."""
        return self.user_service.withdraw(user_uuid)
