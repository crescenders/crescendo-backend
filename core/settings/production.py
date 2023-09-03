from .default import *

CSRF_TRUSTED_ORIGINS = [
    os.environ["API_SERVER_DNS"],
    os.environ["API_SERVER_IP"],
]

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    os.environ["API_SERVER_IP"],
    os.environ["API_SERVER_DNS"],
]
