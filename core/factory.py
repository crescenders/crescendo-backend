import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from crescendo.auth import auth_api, user_container

from . import cli
from .extensions import db, jwt, ma, migrate


def create_app(is_testing: bool = False) -> Flask:
    """Flask Application factory"""
    # 기본 Application 생성
    app = Flask("crescendo-backend")

    # cli 등록
    configure_cli(app=app)

    # 환경 변수 로딩
    set_dotenv()

    # config 설정
    set_config(is_testing, app)

    # CORS 설정
    set_cors(app=app)

    # extensions 등록
    configure_extensions(app=app)

    # Flask-Smorest API 생성
    api = create_api(app=app)

    # namespace 등록
    register_blueprints(api)

    # model 등록
    import_models()

    # DI Container 등록
    set_container(app=app)

    return app


def create_api(app):
    return Api(app)


def set_dotenv():
    load_dotenv(".env", verbose=True)


def configure_extensions(app):
    """Flask extensions 등록"""
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    # Sqlite 에러 제거용
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


def register_blueprints(api):
    """API 에 Namespace 등록"""
    api.register_blueprint(auth_api, url_prefix="/api/v1/auth")


def set_config(is_testing, app: Flask):
    """config 설정"""
    env = os.environ.get("FLASK_DEBUG")
    if env == "1":
        app.config.from_object("core.config.dev")
    else:
        app.config.from_object("core.config.prod")
    if is_testing is True:
        app.config.from_object("core.config.test")


def configure_cli(app):
    """cli 등록"""
    app.cli.add_command(cli.init_app)
    app.cli.add_command(cli.createadminuser)


def set_cors(app):
    cors = CORS(app)  # noqa: F841


def import_models() -> None:
    """Flask-Migrate 를 위한 model import"""
    from crescendo.auth.models import UserModel  # noqa: F401
    from crescendo.study.models import StudyModel  # noqa: F401


def set_container(app) -> None:
    """Container 설정"""
    app.user_container = user_container
