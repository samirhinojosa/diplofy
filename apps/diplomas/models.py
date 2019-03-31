from django.db import models
from django.utils.text import slugify
from django.urls import reverse 
from apps.utils.models import TimeStampedAuthModel
from apps.utils.utils import compress_image, thumbnail_image
from .helpers import upload_to_image_post, upload_to_thumbnail_post


class Issuer(TimeStampedAuthModel):
    """
    Store a issuer

    Open Badges specification of Issuer
    https://www.imsglobal.org/sites/default/files/Badges/OBv2p0Final/index.html#Profile

    Missing fields: type, publicKey, verification, revocationList
    """
    name = models.CharField('Issuer', max_length=150, unique=True, help_text='Name of the issuer')
    url = models.URLField('Website', max_length=200, unique=True, help_text='Website of the issuer')
    slug = models.SlugField('Slug', max_length=100, db_index=True, unique=True, help_text='Name of the issuer in format URL')
    telephone = models.CharField('Telephone', max_length=50, blank=True, help_text='Telephone of the issuer')
    description = models.TextField('Description', max_length=1000, blank=True, help_text="Enter a brief description of the issuer")
    image = models.ImageField('Image', max_length=100, blank=True, upload_to=upload_to_image_post, help_text='Image of the issuer')
    image_thumb = models.ImageField('Thumbnail', max_length=100, blank=True, upload_to=upload_to_thumbnail_post, help_text='Thumbnail of the post')
    email = models.EmailField('Email', max_length=150, blank=True, help_text='Email of the issuer')
    location = models.CharField('Location', max_length=250, blank=True, help_text='Location of the issuer')

    class Meta:
        ordering = ['name']
        verbose_name = 'Issuer'
        verbose_name_plural = 'Issuers'
 
    def __str__(self):
        return (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        if self.pk is not None:
            orig = Issuer.objects.get(pk=self.pk)
            if orig.image != self.image:
                self.image = compress_image(self.image)            
                self.image_thumb = thumbnail_image(self.image)
        else:
            self.image = compress_image(self.image)
            self.image_thumb = thumbnail_image(self.image)
                 
        super(Issuer, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('issuer', args=[str(self.id)])


    












