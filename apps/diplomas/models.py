import uuid
from django.db import models
from django.utils.text import slugify
from django.urls import reverse 
from apps.utils.models import TimeStampedAuthModel
from apps.utils.utils import compress_image, thumbnail_image
from .helpers import (
    issuer_image, 
    issuer_image_thumb, 
    badge_image, 
    badge_image_thumb, 
    badge_image_linkedin, 
    badge_image_linkedin_thumb
)


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

        if self.created:
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
    Store a simple Tag, related to Diploma
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


class Event(TimeStampedAuthModel):
    """
    Store a event

    Open Badges specification of Badge
    https://www.imsglobal.org/sites/default/files/Badges/OBv2p0Final/index.html#BadgeClass

    Missing fields: type, alignment
    """
    #choices
    BADGE, CERTIFICATE = ('B', 'C')
    DIPLOMA_TYPES = (
        (CERTIFICATE, 'Certificate'),
        (BADGE, 'Badge'),
    )

    name = models.CharField('Event', max_length=150, help_text='Name of the event')
    slug = models.SlugField('Slug', max_length=150, help_text='Name of the event in format URL')
    url = models.URLField('Website', max_length=200, blank=True, help_text='Website of the event')
    diploma_type = models.CharField('Type of diploma', max_length=1, choices=DIPLOMA_TYPES,
                    default=BADGE) 
    description = models.TextField('Description', max_length=500, blank=True, 
                    help_text='Enter a brief description of the event')
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE, help_text="Event's issuer")
    tags = models.ManyToManyField(Tag, related_name='events_tags', help_text="Tags of the event")
    location = models.CharField('Location', max_length=150, blank=True, help_text='Location of the event')
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return '%s - %s' % (self.name, self.issuer.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)                
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event', args=[str(self.id)])


class Diploma(TimeStampedAuthModel):
    """
    Store detail of a diploma, related to Diploma
    """    
    #choices
    ASSISTANT, GUESTSPEAKER = ('A', 'G')
    PARTICIPANT_TYPES = (
        (ASSISTANT, 'Assistant'),
        (GUESTSPEAKER, 'Guest Speaker'),
    )

    id = models.UUIDField('Id', primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text='Event')
    participant_type = models.CharField('Type of participant', max_length=1, choices=PARTICIPANT_TYPES)
    criteria = models.TextField('Criteria', max_length=700, blank=True, 
                help_text="Enter the diploma's criteria separated by '|'")
    
    ########## if diploma is a badge.
    img_badge = models.ImageField('Badge', max_length=250, blank=True, upload_to=badge_image, 
                    help_text='Image of the badge')
    img_badge_thumb = models.ImageField('Thumbnail', max_length=250, blank=True, upload_to=badge_image_thumb, 
                    help_text='Thumbnail of the badge')
    # In future, linkedin's (img_badge_in) badge must be done based on main image
    img_badge_in = models.ImageField('Badge for Linkedin', max_length=250, blank=True, 
                        upload_to=badge_image_linkedin, help_text='Image for Linkedin of the badge')
    img_badge_in_thumb = models.ImageField('Thumbnail for Linkedin', max_length=250, blank=True, 
                            upload_to=badge_image_linkedin_thumb, help_text='Thumbnail for Linkedin of the badge')
    ########## if diploma is a certificate. 
    """ 
    img_certificate = models.ImageField('Image', max_length=250, blank=True, upload_to=certificate_image, help_text='Image of the diploma') 
    Unlike badge, certificate must be done for each assertion               
    """

    class Meta:
        ordering = ['-created']
        verbose_name = 'Diploma'
        verbose_name_plural = 'Diplomas'

    def __str__(self):
        return '%s' % (self.get_participant_type_display())

    def save(self, *args, **kwargs):

        if self.created:
            orig = Diploma.objects.get(pk=self.pk)
            if orig.img_badge != self.img_badge:
                self.img_badge = compress_image(self.img_badge)            
                self.img_badge_thumb = thumbnail_image(self.img_badge)
            elif orig.img_badge_in != self.img_badge_in:
                self.img_badge_in = compress_image(self.img_badge_in)            
                self.img_badge_in_thumb = thumbnail_image(self.img_badge_in)
        else:
            if self.img_badge != '':
                self.img_badge = compress_image(self.img_badge)
                self.img_badge_thumb = thumbnail_image(self.img_badge)
            elif self.img_badge_in != '':
                self.img_badge_in = compress_image(self.img_badge_in)            
                self.img_badge_in_thumb = thumbnail_image(self.img_badge_in)
                 
        super(Diploma, self).save(*args, **kwargs)


class Recipient(TimeStampedAuthModel):
    """
    Store a user's recipient

    In future, this should be in the Custom User Model
    """
    first_name = models.CharField('First name', max_length=150, help_text='First name of the user')
    last_name = models.CharField('Last name', max_length=150, help_text='Last name of the user')
    telephone = models.CharField('Telephone', max_length=50, blank=True, help_text='Telephone of the issuer')
    email = models.EmailField('Email', max_length=100, unique=True, help_text='Email of the issuer')

    class Meta:
        ordering = ['-created']
        verbose_name = "Recipient"
        verbose_name_plural = "Recipients"

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Assertion(TimeStampedAuthModel):
    """
    Store a assertion

    Open Badges specification of Badge
    https://www.imsglobal.org/sites/default/files/Badges/OBv2p0Final/index.html#Assertion

    Missing fields: type, verification, image, evidence, narrative, revoked, revocationReason
    """
    licence = models.CharField('License', max_length=150, unique=True, help_text='Generated automatically')
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, help_text='Recipient')
    diploma = models.ForeignKey(Diploma, on_delete=models.CASCADE, help_text='Diploma')
    issued_on = models.DateField('Issued on', null=True, help_text="Issued's day")
    expires = models.DateField('Expires on', null=True, blank=True, help_text="Expired's day")
    short_url = models.URLField("Short url", max_length=200, blank=True, help_text="Assertion's short url")
    sent = models.BooleanField('Sent', default=False, help_text="If it's false, the assertion hasn't been sent")
    
    # if diploma is a certificate. 
    """ 
    Unlike badge, certificate must be done for each assertion               
    """

    class Meta:
        unique_together = [
            ('recipient', 'diploma') 
        ]
        ordering = ['-created']
        verbose_name = "Assertion"
        verbose_name_plural = "Assertions"

    def __str__(self):
        return '%s %s' % (self.recipient.first_name, self.recipient.last_name)

    def save(self, *args, **kwargs):

        if not self.created:
            licence = ''
            while not licence:
                licence = uuid.uuid1().int>>64
                if not Assertion.objects.filter(licence=licence).exists():
                    self.licence = licence
                else:
                    licence = ''
                 
        super(Assertion, self).save(*args, **kwargs)