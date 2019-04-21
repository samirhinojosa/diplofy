from .base import *


ALLOWED_HOSTS = ['165.22.70.66']


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
