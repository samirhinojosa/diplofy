from .base import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = []

# Development's database settings

DB_USER = 'postgres'
DB_NAME = 'postgres'
DB_HOST = 'db'
DB_PASSWORD = 'LocalPassword'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': f'{DB_USER}',
        'PASSWORD': DB_PASSWORD,
        'HOST': f'{DB_HOST}',
        'PORT': '',
    }
}