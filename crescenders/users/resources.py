from flask import request
from flask_restx import Resource, abort

from core.schemas.paginate import PaginateSchema
from crescenders.users import user_resource
from crescenders.users.schemas import UserSchema
from crescenders.users.services import UserService


@user_resource.route("/")
class UserList(Resource):
    def __init__(self, *args, **kwargs):
        self.paginate_schema = PaginateSchema()
        self.user_schema = UserSchema()
        self.user_service = UserService()
        super().__init__(*args, **kwargs)

    def get(self):
        """사용자 전체 목록을 조회합니다.
        pagination 혹은 filter 결과가 있을 경우도 처리합니다."""
        errors = self.paginate_schema.validate(request.args)
        if errors:
            return abort(400, description=errors)
        return self.user_service.get_all_users()

    def post(self):
        """사용자 한 명을 생성합니다.
        비밀번호를 암호화하여 저장합니다."""

        return self.user_service.create_user(**request.json)


@user_resource.route("/<uuid:user_uuid>/")
class UserDetail(Resource):
    def get(self, user_uuid):
        """UUID 로 특정되는 사용자 한 명의 정보를 조회합니다."""
        return user_service.get_one_user(user_uuid)

    def put(self, user_uuid):
        """UUID로 특정되는 사용자 한 명의 정보를 수정합니다."""
        return user_service.update_user(user_uuid, **request.json)

    def delete(self, user_uuid):
        """UUID로 특정되는 사용자 한 명을 삭제합니다."""
        return user_service.withdraw(user_uuid)
