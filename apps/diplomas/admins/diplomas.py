from django.contrib import admin
from django.utils.safestring import mark_safe
from apps.df_auth.models import User
from apps.utils.admin import CSSAdminMixin
from ..models import Diploma, Event, Assertion


class AssertionInline(admin.TabularInline):
    """
    Django admin of Assertion
    """
    model = Assertion
    max_num = 0
    readonly_fields = [
        'id', 'email', 'licence', 'issued_on', 'sent', 'created', 'created_by'
    ]
    fields = [
        'id', 'email', 'licence', 'issued_on', 'sent', 'created', 'created_by',         
    ]

    def email(self, obj):
        return obj.recipient.email

    def slug(self, obj):
        return obj.user.slug
    
    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()

class DiplomaAdmin(admin.ModelAdmin, CSSAdminMixin):
    """
    Django admin of Diploma
    """

    #inlines = [AssertionInline]
    
    list_display = [
        'thumbnail', 'issuer', 'event_name', 'participant_type', 'id', 'created', 'created_by'
    ] 
    list_display_links = [
        'thumbnail', 'event_name', 'id'
    ] 
    list_filter = [
        'event__name', 'event__issuer__name', 'participant_type', 'created'
    ]
    search_fields = [
        'event__name', 'event__issuer__name', 'created_by'
    ]
    readonly_fields = [
        'id', 'thumbnail', 'linkedin_thumb', 'issuer',
        'created', 'created_by', 'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Event", {
            'fields': (('issuer', 'event'))
        }),
        ("Diploma's details", {
            'fields': (('participant_type', 'id'), 'criteria')
        }),
        ("Diploma's main image", {
            'fields': ('img_badge', 'thumbnail')
        }),
        ("Diploma's image for linkedin", {
            'fields': ('img_badge_in', 'linkedin_thumb')
        }),

        ('Audit', {
            'classes': ('collapse',),
            'fields': (('created', 'created_by'), ('modified', 'modified_by'))
        }),
    ]

    def issuer(self, obj):
        return obj.event.issuer

    def event_name(self, obj):
        return obj.event.name

    def thumbnail(self, obj):
        """ Get the diplomas's thumbnail in the admin """

        if obj.img_badge_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="auto" >'.format(url = obj.img_badge_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/static/not-available.png" width="75" height="75" >'
            )
    
    def linkedin_thumb(self, obj):
        """ Get the diploma's thumbnail for linkedin in the admin """

        if obj.img_badge_in_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="150" height="auto" >'.format(url = obj.img_badge_in_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/static/not-available.png" width="75" height="75" >'
            )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()