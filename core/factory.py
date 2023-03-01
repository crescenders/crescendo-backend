from flask import Flask
from flask_smorest import Api

from crescenders.auth.resources import blp as auth_blp

from .extensions import db, jwt, migrate


def create_app():
    app = Flask(__name__)
    set_config(app)
    configure_extensions(app=app)
    api = Api(app)
    register_blueprints(api)
    return app


def configure_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(api):
    api.register_blueprint(auth_blp)


def set_config(app):
    app.config.from_object("core.config.dev")
