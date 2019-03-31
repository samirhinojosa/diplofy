from django.db import models

class SubscriptionBase(models.Model):
    """
    Store the email of a future customer 
    """
    email = models.EmailField('Email', max_length=150, blank=True, help_text='Email of the issuer')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Interested'
        verbose_name_plural = 'Interested'
 
    def __str__(self):
        return (self.email)