from .base import *



ALLOALLOWED_HOSTS = ['159.203.41.156']


# Development's database settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'diplofy_db',
        'USER': 'diplofy_usr',
        'PASSWORD': 'diplofy_pwd',
        'HOST': 'db',                     
        'PORT': '5432', 
    }
}

