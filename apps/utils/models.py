from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base class which store a creation and modification date and time
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TimeStampedAuthModel(TimeStampedModel):
    """
    Abstract base class which store a creation and modification user
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, 
                        related_name='%(app_label)s_%(class)s_created_by')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, 
                        related_name='%(app_label)s_%(class)s_modified_by')

    class Meta:
        abstract = True
