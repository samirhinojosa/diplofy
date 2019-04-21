from .base import *


ALLOWED_HOSTS = ['165.22.65.171', 'localhost']


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