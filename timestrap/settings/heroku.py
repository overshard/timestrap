import dj_database_url
import os

from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY'] 


DEBUG = False


DATABASES = {
    'default': dj_database_url.config(conn_max_age=500)
}
