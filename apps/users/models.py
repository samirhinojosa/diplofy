from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    """
    Store a custom user
    """
    pass
   """  #app_label = 'auth'

class Group(Group):
    pass

    class Meta:
    #app_label = 'authentication'

 class ProxyUser(User):
     pass

     class Meta:
         #app_label = 'auth'
         proxy = True
         verbose_name = 'User'
         verbose_name_plural = 'Users' """