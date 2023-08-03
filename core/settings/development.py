from .default import *

DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE

INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
