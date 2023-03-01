from flask.views import MethodView
from flask_smorest.blueprint import Blueprint

blp = Blueprint(
    "auth_api", __name__, description="authentication api", url_prefix="/api"
)


@blp.route("/")
class LoginAPIView(MethodView):
    @blp.response(404)
    def get(self):
        return {"message": "Hello, World!"}
