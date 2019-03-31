from django.conf import settings
from django.utils.text import slugify


def upload_to_image(self, filename, flag):
    """
    Stores the image in a specific path regards object's name & class

    Structure of paths:
        - diplomas/issuer/
        - diplomas/issuer/thumbnail        
        - diplomas/badges/nombredelissuer/
        - diplomas/badges/nombredelissuer/thumbnail
        - diplomas/badges/nombredelissuer/linkedin
        - diplomas/badges/nombredelissuer/linkedin/thumbnail
    """ 
    ext = filename.split('.')[-1]
    name = slugify(self.name)
    file_path = ''
    filename = ''

    if self.__class__.__name__ == 'Issuer':
        if flag == 'image':
            file_path = 'diplomas/issuers/'
            filename = '%s.%s' % (name, ext)
        elif flag == 'thumb': 
            file_path = 'diplomas/issuers/thumbnails/'
            filename = '%s_thumb.%s' % (name, ext)
    elif self.__class__.__name__ == 'Badge':
        if flag == 'image':
            file_path = 'diplomas/badges/%s/' % (self.issuer.slug)
            filename = '%s.%s' % (name, ext)
        elif flag == 'thumb': 
            file_path = 'diplomas/badges/%s/thumbnails/' % (self.issuer.slug)
            filename = '%s_thumb.%s' % (name, ext)
        elif flag == 'linkedin': 
            file_path = 'diplomas/badges/%s/linkedin/' % (self.issuer.slug)
            filename = '%s_in.%s' % (name, ext)
        elif flag == 'linkedin_thumb': 
            file_path = 'diplomas/badges/%s/linkedin/thumbnails/' % (self.issuer.slug)
            filename = '%s_in_thumb.%s' % (name, ext)

    return '%s/%s/%s' % (settings.MEDIA_ROOT, file_path, filename)


def issuer_image(instance, filename):
    return upload_to_image(instance, filename, 'image')

def issuer_image_thumb(instance, filename):
    return upload_to_image(instance, filename, 'thumb')

def badge_image(instance, filename):
    return upload_to_image(instance, filename, 'image')

def badge_image_thumb(instance, filename):
    return upload_to_image(instance, filename, 'thumb')

def badge_image_linkedin(instance, filename):
    return upload_to_image(instance, filename, 'linkedin')

def badge_image_linkedin_thumb(instance, filename):
    return upload_to_image(instance, filename, 'linkedin_thumb')