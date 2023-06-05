from fullask_rest_framework.factory.app_factory import BaseApplicationFactory


class CrescendoApplicationFactory(BaseApplicationFactory):
    FLASK_APP_NAME = "crescendo-backend"
    APP_BASE_DIR = "crescendo"
    CONFIG_FILE = "core.config.dev"
    EXTENSION_FILE = "fullask_rest_framework.factory.extensions"
    MICRO_APP_CONFIG = [
        {"crescendo.auth": "/api/v1/auth/"},
    ]
