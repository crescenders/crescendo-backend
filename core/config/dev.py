from os.path import join

from core.config.default import *

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(join(BASE_DIR, "db.sqlite"))
