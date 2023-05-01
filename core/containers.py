from dependency_injector import containers, providers
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    app = providers.Dependency(instance_of=Flask)
    db = providers.Dependency(instance_of=SQLAlchemy)
    migrate = providers.Dependency(Migrate)
    jwt = providers.Dependency(JWTManager)
    ma = providers.Dependency(Marshmallow)
