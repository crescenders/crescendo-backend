from logging.config import dictConfig
from os.path import join

from factory.config.default import *  # noqa: F403

DEBUG = False

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
    join(BASE_DIR, "db.sqlite3")  # noqa: F405
)

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)s - %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            },
            "file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(BASE_DIR, "logs/error.log"),
                "maxBytes": 1024 * 1024 * 5,  # 5 MB
                "backupCount": 5,
                "formatter": "default",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["wsgi", "file"],
        },
    }
)
