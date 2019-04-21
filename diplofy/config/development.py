from .base import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True


# Development's database settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'diplofy_db',
        'USER': 'diplofy_usr',
        'PASSWORD': 'diplofy_pwd',
        'HOST': 'db',                     
        'PORT': '5432', 
    }
}