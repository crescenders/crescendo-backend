from .default import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
    }
}

CSRF_TRUSTED_ORIGINS = [
    f"https://{os.environ['API_SERVER_DNS']}",
]

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    os.environ["API_SERVER_IP"],
    os.environ["API_SERVER_DNS"],
]
