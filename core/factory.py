import os

from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from crescendo.auth import auth_api

from . import cli
from .extensions import db, jwt, ma, migrate


def create_app():
    """Flask Application factory"""

    # 기본 Application 생성
    app = Flask("crescendo-backend")

    # config 설정
    set_config(app=app)

    # CORS 설정
    set_cors(app=app)

    # extensions 등록
    configure_extensions(app=app)

    # Flask-Smorest API 생성
    api = create_api(app=app)

    # cli 등록
    configure_cli(app=app)

    # namespace 등록
    register_blueprints(api)

    # model 등록
    import_models()

    return app


def create_api(app):
    return Api(app)


def configure_extensions(app):
    """Flask extensions 등록"""
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(api):
    """API 에 Namespace 등록"""
    api.register_blueprint(auth_api, url_prefix="/api/v1/auth")


def set_config(app):
    """config 설정"""
    env = os.environ.get("FLASK_DEBUG")
    if env == "1":
        app.config.from_object("core.config.dev")
    else:
        app.config.from_object("core.config.prod")


def configure_cli(app):
    """cli 등록"""
    app.cli.add_command(cli.init_app)


def set_cors(app):
    cors = CORS(app)


def import_models() -> None:
    """Flask-Migrate 를 위한 model import"""
    from crescendo.auth.models import UserModel
