#########################
# Define your Blueprint.#
#########################
from flask.views import MethodView
from flask_smorest import Blueprint

STUDY_MICRO_APP = Blueprint(
    name="StudyAPI",
    import_name=__name__,
    url_prefix="",
    description="스터디, 카테고리, 태그 관리를 위한 API 입니다.",
)


@STUDY_MICRO_APP.route("/categories")
class CategoryListAPI(MethodView):
    def get(self):
        pass

    def post(self):
        pass


class CategoryDetailAPI(MethodView):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
