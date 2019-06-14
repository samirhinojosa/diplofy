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

# Development's email settings


# https://www.youtube.com/watch?v=X7DWErkNVJs
# https://blog.mailtrap.io/sending-emails-in-python-tutorial-with-code-examples/
# https://mailtrap.io/inboxes/621778/settings

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '0811bcd07fe723'
EMAIL_HOST_PASSWORD = 'f16c396d318323'
EMAIL_PORT = '2525'

# In Productions should be 0
EMAIL_SLEEP = 11