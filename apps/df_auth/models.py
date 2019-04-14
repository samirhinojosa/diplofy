from django.db import models
from django.contrib.auth.models import AbstractUser, Group
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

class ProxyGroup(Group):
    pass

    class Meta:
        app_label = 'auth'
        proxy = True
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'