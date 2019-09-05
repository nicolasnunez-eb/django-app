from .base import *  # noqa
from . import get_env_variable
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}

DB_FROM_ENV = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(DB_FROM_ENV)

SOCIAL_AUTH_EVENTBRITE_KEY = get_env_variable('SOCIAL_AUTH_EVENTBRITE_KEY')
SOCIAL_AUTH_EVENTBRITE_SECRET = get_env_variable(
    'SOCIAL_AUTH_EVENTBRITE_SECRET',
)
