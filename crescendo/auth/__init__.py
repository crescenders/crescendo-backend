from flask_smorest import Blueprint

auth_api = Blueprint(
    "auth",
    "auth,",
    description="인증 서비스를 다루는 API입니다.",
)
