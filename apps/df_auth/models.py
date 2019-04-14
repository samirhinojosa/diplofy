from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Store a custom user
    """
    pass

class ProxyUser(User):
    pass

    class Meta:
        app_label = 'auth'
        proxy = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'