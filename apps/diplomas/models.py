from django.db import models
from django.utils.text import slugify
from django.urls import reverse 
from apps.utils.models import TimeStampedAuthModel
from apps.utils.utils import compress_image, thumbnail_image
from .helpers import (issuer_image, issuer_image_thumb, badge_image, badge_image_thumb, 
                        badge_image_linkedin, badge_image_linkedin_thumb)


class Issuer(TimeStampedAuthModel):
    """
    Store a issuer

    Open Badges specification of Issuer
    https://www.imsglobal.org/sites/default/files/Badges/OBv2p0Final/index.html#Profile

    Missing fields: type, publicKey, verification, revocationList
    """
    name = models.CharField('Issuer', max_length=150, help_text='Name of the issuer')
    url = models.URLField('Website', max_length=200, blank=True, help_text='Website of the issuer')
    slug = models.SlugField('Slug', max_length=150, help_text='Name of the issuer in format URL')
    telephone = models.CharField('Telephone', max_length=50, blank=True, help_text='Telephone of the issuer')
    description = models.TextField('Description', max_length=500, blank=True, help_text='Enter a brief description of the issuer')
    image = models.ImageField('Image', max_length=250, blank=True, upload_to=issuer_image, 
                help_text='Image of the issuer')
    image_thumb = models.ImageField('Thumbnail', max_length=250, blank=True, upload_to=issuer_image_thumb, 
                    help_text='Thumbnail of the post')
    email = models.EmailField('Email', max_length=100, blank=True, help_text='Email of the issuer')
    location = models.CharField('Location', max_length=150, blank=True, help_text='Location of the issuer')

    class Meta:
        ordering = ['-created']
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
            if self.image != '':
                self.image = compress_image(self.image)
                self.image_thumb = thumbnail_image(self.image)
                 
        super(Issuer, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('issuer', args=[str(self.id)])


class Tag(TimeStampedAuthModel):
    """
    Store a simple Tag, related to Badge
    """
    name = models.CharField('Tag', max_length=150, unique=True, help_text='Name of the tag')
    slug = models.SlugField('Slug', max_length=150, db_index=True, unique=True, 
            help_text='Name of the tag in format URL')

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
 
    def __str__(self):
        return (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) 
        super(Tag, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('tag', args=[str(self.id)])

class Badge(TimeStampedAuthModel):
    """
    Store a badge

    Open Badges specification of Badge
    https://www.imsglobal.org/sites/default/files/Badges/OBv2p0Final/index.html#BadgeClass

    Missing fields: type, alignment
    """
    name = models.CharField('Badge', max_length=150, help_text='Name of the badge')
    url = models.URLField('Website', max_length=200, blank=True, help_text='Website of the badge')
    slug = models.SlugField('Slug', max_length=150, help_text='Name of the badge in format URL')
    description = models.TextField('Description', max_length=500, blank=True, 
                    help_text='Enter a brief description of the badge')
    image = models.ImageField('Image', max_length=250, blank=True, upload_to=badge_image, 
                    help_text='Image of the badge')
    image_thumb = models.ImageField('Thumbnail', max_length=250, blank=True, upload_to=badge_image_thumb, 
                    help_text='Thumbnail of the badge')
    image_linkedin = models.ImageField('Image for Linkedin', max_length=250, blank=True, 
                        upload_to=badge_image_linkedin, help_text='Image for Linkedin of the badge')
    image_linkedin_thumb = models.ImageField('Thumbnail for Linkedin', max_length=250, blank=True, 
                            upload_to=badge_image_linkedin_thumb, help_text='Thumbnail for Linkedin of the badge')
    criteria = models.TextField('Criteria', max_length=700, blank=True, 
                help_text="Enter the badge's criteria separeted by '|'")
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE, help_text="Badge's issuer")
    location = models.CharField('Location', max_length=150, blank=True, help_text='Location of the badge')
    tags = models.ManyToManyField(Tag, related_name='badges_tags', help_text='Tags of the badge')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'

    def __str__(self):
        return (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        if self.pk is not None:
            orig = Badge.objects.get(pk=self.pk)
            if orig.image != self.image:
                self.image = compress_image(self.image)            
                self.image_thumb = thumbnail_image(self.image)
            elif orig.image_linkedin != self.image_linkedin:
                self.image_linkedin = compress_image(self.image_linkedin)            
                self.image_linkedin_thumb = thumbnail_image(self.image_linkedin)
        else:
            if self.image != '':
                self.image = compress_image(self.image)
                self.image_thumb = thumbnail_image(self.image)
            elif self.image_linkedin != '':
                self.image_linkedin = compress_image(self.image_linkedin)            
                self.image_linkedin_thumb = thumbnail_image(self.image_linkedin)
                 
        super(Badge, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('badge', args=[str(self.id)])