from .base import *  # noqa: F403


DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = "CHANGE-ME"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),  # noqa: F405
    }
}


# Channels
# https://channels.readthedocs.io/en/latest/

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("localhost", 6379)]},
    }
}


# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
