import importlib

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api


class ApplicationFactory:
    FLASK_APP_NAME = "crescendo-backend"
    APP_BASE_DIR = "crescendo"
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
        {"crescendo.auth": "/api/v1/auth/"},
    ]

    @classmethod
    def create_app(cls):
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
        # register micro apps. this also does the Dependency Injection.
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
        if cls.CONFIG_FILE:
            flask_app.config.from_object(importlib.import_module(cls.CONFIG_FILE))
        else:
            pass

    @classmethod
    def _configure_extensions(cls, flask_app):
        """
        configure third-party extensions, with `EXTENSION_FILE`.
        """

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
        this also does the Dependency Injection,
        with dependency_injector's DynamicContainer.
        """

        for micro_app_information in cls.MICRO_APP_CONFIG:
            for app_package_string, url_prefix in micro_app_information.items():
                app_package_module = importlib.import_module(app_package_string)
                # Register Blueprint.
                smorest_api.register_blueprint(
                    app_package_module.BLUEPRINT,
                    url_prefix=url_prefix,
                )
                # get the microapp container.
                cls._setup_di_container(
                    micro_app_container=app_package_module.MICROAPP_CONTAINER
                )

    @classmethod
    def _setup_di_container(cls, micro_app_container):
        # wiring the DI Container.
        micro_app_container.wire(packages=[cls.APP_BASE_DIR])
