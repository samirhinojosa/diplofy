from django.conf import settings
from django.utils.text import slugify
from datetime import datetime


def upload_to_image_post(self, filename):
    """
    Stores the issuer's image in a specific path regards its name
    """    
    ext = filename.split('.')[-1]
    name = slugify(self.name) 

    filename = '%s.%s' % (name, ext)

    return '%s/diplomas/issuers/%s' % (settings.MEDIA_ROOT, filename)


def upload_to_thumbnail_post(self, filename):
    """
    Stores the issuer's thumbnail in a specific its name
    """    
    ext = filename.split('.')[-1]
    name = slugify(self.name) 

    filename = "%s_thumb.%s" % (name, ext)
  
    return '%s/diplomas/issuers/thumbnail/%s' % (settings.MEDIA_ROOT, filename)