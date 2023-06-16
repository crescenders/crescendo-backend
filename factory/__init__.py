from fullask_rest_framework.factory.app_factory import BaseApplicationFactory


class CrescendoApplicationFactory(BaseApplicationFactory):
    FLASK_APP_NAME = "crescendo-backend"
    APP_BASE_DIR = "crescendo"
    DOTENV_SETTINGS = {"dotenv_path": ".env"}
    CONFIG_MAPPING = {
        "dev": {
            "from_object": {"obj": "factory.config.dev"},
        },
        "test": {
            "from_object": {"obj": "factory.config.test"},
        },
    }
    EXTENSION_MODULE = "fullask_rest_framework.factory.extensions"
    MICRO_APP_CONFIG = [
        {"crescendo.auth": "/api/v1/auth/"},
        {"crescendo.study": "/api/v1/studies/"},
    ]
