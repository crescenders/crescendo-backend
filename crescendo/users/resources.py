from flask import request
from flask_restx import Resource, abort, reqparse

from crescendo.users import user_resource
from crescendo.users.marshallers import BaseUserMarshaller
from crescendo.users.services import UserService

# TODO : DI 적용하기
user_list_marshaller = user_resource.model(
    "UserList", BaseUserMarshaller.to_model_dict()
)

parser = reqparse.RequestParser()
parser.add_argument("size", type=int, required=False, location="args", help="페이지의 크기")
parser.add_argument("page", type=int, required=False, location="args", help="페이지의 숫자")
parser.add_argument("query", type=str, required=False, location="args", help="검색어")


@user_resource.route("/")
class UserList(Resource):
    def __init__(self, *args, **kwargs):
        self.user_service = UserService()
        super().__init__(*args, **kwargs)

    @user_resource.marshal_list_with(user_list_marshaller)
    @user_resource.doc(parser=parser)
    def get(self):
        """사용자 전체 목록을 조회합니다.
        pagination 혹은 filter 결과가 있을 경우도 처리합니다."""

        return self.user_service.get_all_users()

    @user_resource.marshal_with(user_list_marshaller)
    @user_resource.expect(user_list_marshaller)
    def post(self):
        """사용자 한 명을 생성합니다.
        비밀번호를 암호화하여 저장합니다."""

        return self.user_service.create_user(**request.json)


@user_resource.route("/<uuid:user_uuid>/")
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
