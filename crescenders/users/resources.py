from flask.views import MethodView
from flask_smorest.blueprint import Blueprint

blp = Blueprint("accounts_api", __name__, description="account api")


@blp.route("/")
class UserListAPIView(MethodView):
    @blp.response(200)
    def get(self):
        return {"message": "user list view."}

    @blp.response(201)
    def post(self):
        return {"message": "create user."}


@blp.route("/<int:user_id>/")
class UserDetailAPIView(MethodView):
    @blp.response(200)
    def get(self, user_id):
        return {"message": f"user detail view, id from request is {user_id}"}

    @blp.response(200)
    def put(self):
        return {"message": "user info update view."}

    @blp.response(204)
    def delete(self):
        return {"message": "delete view."}
