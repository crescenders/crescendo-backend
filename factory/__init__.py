from fullask_rest_framework.factory.app_factory import BaseApplicationFactory


class CrescendoApplicationFactory(BaseApplicationFactory):
    FLASK_APP_NAME = "crescendo-backend"
    DOTENV_SETTINGS = {"dotenv_path": ".env"}
    CONFIG_MAPPING = {
        "prod": {
            "from_object": {"obj": "factory.config.prod"},
        },
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
        {"crescendo.study": "/api/v1/study/"},
    ]
