from .base import *


# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['backoffice.diplofy.com', '178.128.237.183', 'localhost']


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