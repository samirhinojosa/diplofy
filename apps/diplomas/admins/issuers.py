from django.contrib import admin
from django.utils.safestring import mark_safe
from apps.df_auth.models import User
from apps.utils.admin import CSSAdminMixin
from ..models import Issuer


class IssuerAdmin(admin.ModelAdmin, CSSAdminMixin):
    """
    Django admin of Issuers
    """
    list_display = [
        'thumbnail', 'name', 
        'created', 'created_by', 'modified', 'modified_by'
    ] 
    list_display_links = [
        'thumbnail', 'name'
    ] 
    list_filter = [
        'created_by', 'created'
    ]
    search_fields = [
        'name', 'location'
    ]
    readonly_fields = [
        'thumbnail', 'slug', 'created', 'created_by', 'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Issuer's details", {
            'fields': (('name', 'slug'), 'url', 'telephone', 'description')
        }),
        ("Issuer's image", {
            'fields': ('image', 'thumbnail')
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': (('created', 'created_by'), ('modified', 'modified_by'))
        }),
    ]

    def thumbnail(self, obj):
        """ Get the issuer's thumbnail in the admin """

        if obj.image_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.image_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/static/not-available.png" width="75" height="75" >'
            )

    def slug(self, obj):
        return obj.user.slug

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()
