import os

from dependency_injector import providers
from flask import Flask
from flask_restx import Api

from crescendo.auth.resources import auth_api
from crescendo.users.container import UserContainer
from crescendo.users.resources import users_api
from crescendo.users.services import UserService, UserServiceABC

from .extensions import db, jwt, ma, migrate


def create_app():
    """Flask Application factory"""

    # 기본 Application 생성
    app = Flask("crescendo-backend")

    # config 설정
    set_config(app)

    # extensions 등록
    configure_extensions(app=app)

    # Flask-RestX API 생성
    api = create_api(app=app)

    # di container 준비
    set_di_container()

    # namespace 등록
    register_namespaces(api)

    # model 등록
    import_models()

    return app


def create_api(app):
    return Api(
        app,
        version="v1",
        title="Crescendo_backend Server API",
        terms_url="/",
        contact="twicegoddessana1229@gmail.com",
        license="MIT",
    )


def configure_extensions(app):
    """Flask extensions 등록"""
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)


def register_namespaces(api):
    """API 에 Namespace 등록"""
    api.add_namespace(users_api, path="/api/v1/users")
    api.add_namespace(auth_api, path="/api/v1/auth")


def set_config(app):
    """config 설정"""
    env = os.environ.get("FLASK_DEBUG")
    if env == "1":
        app.config.from_object("core.config.dev")
    else:
        app.config.from_object("core.config.prod")


def import_models() -> None:
    """Flask-Migrate 를 위한 model import"""
    from crescendo.users.models import User


def set_di_container() -> None:
    user_container = UserContainer(user_service_abc=providers.Singleton(UserService))
