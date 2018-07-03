from .base import *  # noqa: F401,F403


DEBUG = False


# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ['SECRET_KEY']  # noqa: F405


# SECURITY WARNING: set this to your domain name in production!

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Email
# TODO: Need to set this up to not just output to console...

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
