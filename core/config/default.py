from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
PROPAGATE_EXCEPTIONS = True

API_TITLE = "Crescendo_backend Server API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.0"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger/"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
OPENAPI_REDOC_PATH = "/redoc/"
OPENAPI_REDOC_URL = "https://rebilly.github.io/ReDoc/releases/latest/redoc.min.js"
OPENAPI_RAPIDOC_PATH = "/rapidoc"
OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"
