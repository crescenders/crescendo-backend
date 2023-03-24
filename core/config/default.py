from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
PROPAGATE_EXCEPTIONS = True

API_TITLE = "crescenders_backend API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.0"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/docs"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
SWAGGER_UI_DOC_EXPANSION = "full"
SWAGGER_UI_OPERATION_ID = True
SWAGGER_UI_REQUEST_DURATION = True

RESTX_MASK_HEADER = None  # field mask 비활성화
RESTX_MASK_SWAGGER = False  # field mask 비활성화
