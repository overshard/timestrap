from .base import *

DEBUG = True

# Used for development compressing testing
COMPRESS_OFFLINE = False
COMPRESS_ENABLED = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGE-ME' 


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
