from os.path import join

from core.config.default import *

TESTING = True
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(join(BASE_DIR, "test_db.sqlite3"))
