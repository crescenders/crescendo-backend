from datetime import timedelta
from urllib.parse import quote_plus

from factory.config.default import *  # noqa: F403

DEBUG = False

JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=3)

SQLALCHEMY_DATABASE_URI = (
    f"oracle+oracledb://{quote_plus(os.environ['DB_USERNAME'])}:{quote_plus(os.environ['DB_PASSWORD'])}@{os.environ['DB_DSN']}"
    f"?config_dir={quote_plus(os.environ['DB_CONFIG_DIR'])}"
    f"&wallet_location={quote_plus(os.environ['DB_WALLET_LOCATION'])}"
    f"&wallet_password={quote_plus(os.environ['DB_WALLET_PASSWORD'])}"
)
