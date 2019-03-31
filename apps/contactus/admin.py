from django.contrib import admin
from .models import SubscriptionBase

class SubscriptionBaseAdmin(admin.ModelAdmin):
    """
    Django admin of interested
    """
    list_display = [
        'email', 'created'
    ] 
    list_display_links = [
        'email'
    ] 
    readonly_fields = [
        'created'
    ]
    fields = [
        'email', 'created'
    ]

admin.site.register(SubscriptionBase, SubscriptionBaseAdmin)
