from os.path import join

from factory.config.default import *  # noqa: F403

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
    join(BASE_DIR, "db.sqlite3")  # noqa: F405
)
