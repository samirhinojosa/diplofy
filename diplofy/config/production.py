from .base import *


# SECURITY WARNING: don't run with debug turned on in production!

#DEBUG = True

ALLOWED_HOSTS = ['159.89.127.112', 'localhost']


# Development's database settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'diplofydb',
        'USER': 'diplofy_usr',
        'PASSWORD': 'Diplo@PWD#DB2019_',
        'HOST': 'localhost',                     
        'PORT': '', 
    }
}