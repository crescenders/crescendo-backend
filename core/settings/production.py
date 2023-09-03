import os

from .default import *

CSRF_TRUSTED_ORIGINS = [
    f"https://{os.environ['API_SERVER_DNS']}",
]
print(CSRF_TRUSTED_ORIGINS)
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    os.environ["API_SERVER_IP"],
    os.environ["API_SERVER_DNS"],
]
