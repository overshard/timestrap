import os

import dj_database_url

from .base import *  # noqa: F401, F403


DEBUG = False


# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ['SECRET_KEY']


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(conn_max_age=500)
}
