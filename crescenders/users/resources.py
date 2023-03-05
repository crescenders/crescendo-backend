from flask.views import MethodView
from flask_smorest.blueprint import Blueprint

from crescenders.users.models import User as UserModel
from crescenders.users.schemas import UserListReadSchema, UserSchema

blp = Blueprint("accounts_api", __name__, description="account api")


@blp.route("/")
class UserListAPIView(MethodView):
    @blp.response(200, UserListReadSchema(many=True))
    def get(self):
        """
        모든 사용자 목록을 조회합니다.

        id, uuid, email, full_name, created_on, updated_on 정보를 조회합니다.
        """
        return UserModel.find_all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self):
        return {"message": "create user."}


@blp.route("/<int:user_id>/")
class UserDetailAPIView(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.find_by_id(user_id)

    @blp.response(200)
    def put(self, user_id):
        return {"message": "user info update view."}

    @blp.response(204)
    def delete(self, user_id):
        return {"message": "delete view."}
