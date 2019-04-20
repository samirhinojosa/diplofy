from .base import *


ALLOALLOWED_HOSTS = ['159.203.41.156']


# Development's database settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'diplofydb',
        'USER': 'diplofy_usr',
        'PASSWORD': 'Diplo@PWD#DB2019_',
        'HOST': 'db',                     
        'PORT': '5432', 
    }
}