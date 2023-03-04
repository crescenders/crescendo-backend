from flask import Flask
from flask_smorest import Api

from crescenders.users.resources import blp as account_blp

from .extensions import db, jwt, migrate


def create_app():
    app = Flask("crescenders-backend")
    set_config(app)
    configure_extensions(app=app)
    api = Api(app)
    register_blueprints(api)
    import_models()
    return app


def configure_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(api):
    api_prefix = "api"
    version = "1"
    api.register_blueprint(account_blp, url_prefix=f"/{api_prefix}/v{version}/users")


def set_config(app):
    app.config.from_object("core.config.dev")


def import_models():
    from crescenders.users.models import User
