import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
PROPAGATE_EXCEPTIONS = True
# SECRET_KEY = os.environ["SECRET_KEY"]
API_TITLE = "Crescendo_backend Server API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.0"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

API_SPEC_OPTIONS = {
    "components": {
        "securitySchemes": {
            "Bearer Auth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "",
            }
        }
    },
}
