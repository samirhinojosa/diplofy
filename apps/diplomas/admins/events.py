from django.contrib import admin
from apps.df_auth.models import User
from apps.utils.admin import CSSAdminMixin
from ..models import Event


class EventAdmin(admin.ModelAdmin, CSSAdminMixin):
    """
    Django admin of Event
    """
    list_display = [
        'name', 'diploma_type', 'issuer', 'location',  
        'created', 'created_by'
    ] 
    list_display_links = [
        'name',
    ] 
    list_filter = [
        'issuer__name', 'diploma_type', 'created', 
    ]
    search_fields = [
        'name', 'location'
    ]
    readonly_fields = [
        'slug', 'created', 'created_by', 'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Diploma's details", {
            'fields': ('issuer', ('name', 'slug'), ('diploma_type', 'tags'), 'url', 'description', 
                         'location')
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': (('created', 'created_by'), ('modified', 'modified_by'))
        }),
    ]

    def slug(self, obj):
        return obj.user.slug

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()