import os

from .default import *

ALLOWED_HOSTS = [
    "127.0.0.1",
    os.environ["API_SERVER_URL"],
]
