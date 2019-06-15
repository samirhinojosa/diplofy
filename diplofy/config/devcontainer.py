from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


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


# Development's mass email settings

EMAIL_HOST = 'mailtrap'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = '25'


# Development's single email settings with tools to details and analysis

""" EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '0811bcd07fe723'
EMAIL_HOST_PASSWORD = 'f16c396d318323'
EMAIL_PORT = '2525' """