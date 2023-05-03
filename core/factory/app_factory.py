import importlib
import inspect
import pkgutil
import sys

from dependency_injector.containers import DynamicContainer
from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api

from core.factory.di import BaseComponent
from core.repositories.base import BaseRepository
from core.resources.base import BaseResource
from core.services.base import BaseService
from crescendo import auth


class ApplicationFactory:
    FLASK_APP_NAME = "crescendo-backend"
    CONFIG_FILE = "core.config.dev"
    EXTENSION_FILE = "core.factory.extensions"
    DOTENV_SETTINGS = {
        "stream": None,
        "verbose": False,
        "override": False,
        "interpolate": True,
        "encoding": "utf-8",
    }
    MICRO_APP_CONFIG = [
        {"crescendo.auth": "/api/v1/auth/something/"},
    ]

    @classmethod
    def create_app(cls):
        app_container = DynamicContainer()
        # load environment variables.
        cls._load_dotenv()
        # create a flask app.
        flask_app = cls._create_flask_app()
        # load flask config, with flask app.
        cls._load_config(flask_app)
        # create a flask-smorest Api object.
        smorest_api = Api(app=flask_app)
        # configure third-party extensions.
        cls._configure_extensions(flask_app=flask_app)
        # register micro apps.
        cls._register_micro_apps(smorest_api)
        return flask_app

    @classmethod
    def _load_dotenv(cls):
        """
        load dotenv file, if cls.DOTENV_SETTINGS is set.
        """
        if cls.DOTENV_SETTINGS:
            load_dotenv(**cls.DOTENV_SETTINGS)

    @classmethod
    def _create_flask_app(cls) -> Flask:
        """
        create flask app, with `FLASK_APP_NAME`.
        """
        if hasattr(cls, "FLASK_APP_NAME"):
            return Flask(cls.FLASK_APP_NAME)
        else:
            raise AttributeError(
                f"`FLASK_APP_NAME` class variable is not set in '{cls.__name__}'"
            )

    @classmethod
    def _load_config(cls, flask_app: Flask):
        """load flask app config."""
        if cls.CONFIG_FILE:
            flask_app.config.from_object(importlib.import_module(cls.CONFIG_FILE))
        else:
            pass

    @classmethod
    def _configure_extensions(cls, flask_app):
        extensions = importlib.import_module(cls.EXTENSION_FILE)
        extension_vars = [
            extension_var
            for extension_var in dir(extensions)
            if not extension_var.startswith("__")
            and not callable(getattr(extensions, extension_var))
        ]
        for var in extension_vars:
            getattr(extensions, var).init_app(flask_app)

    @classmethod
    def _register_micro_apps(cls, smorest_api):
        """
        register micro apps, with cls.MICRO_APP_CONFIG settings.
        """
        for micro_app in cls.MICRO_APP_CONFIG:
            for app_package, url_prefix in micro_app.items():
                micro_app_blueprint = importlib.import_module(
                    f"{app_package}"
                ).BLUEPRINT
                smorest_api.register_blueprint(
                    micro_app_blueprint, url_prefix=url_prefix
                )


# def find_abs_modules(module):
#     path_list = []
#     spec_list = []
#     for importer, modname, ispkg in pkgutil.walk_packages(module.__path__):
#         import_path = f"{module.__name__}.{modname}"
#         if ispkg:
#             spec = pkgutil._get_spec(importer, modname)
#             importlib._bootstrap._load(spec)
#             spec_list.append(spec)
#         else:
#             path_list.append(import_path)
#     for spec in spec_list:
#         del sys.modules[spec.name]
#     return path_list
#
#
# app_modules = find_abs_modules(auth)
# for mod in app_modules:
#     print(importlib.import_module(mod))


########
# components = inspect.getmembers(auth, inspect.isclass)
# for component in components:
#     print(f"{component[1]} : {issubclass(component[1], BaseComponent)}")
