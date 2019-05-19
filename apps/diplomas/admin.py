from django.contrib.admin import AdminSite
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportMixin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields, resources
from apps.df_auth.models import User
from apps.utils.admin import FilterUserAdmin, CSSAdminMixin, DiplofyAdminSite
from .models import Issuer, Diploma, DiplomaDetail, Tag, Recipient, Assertion

from .admins.issuers import IssuerAdmin
from .admins.tags import TagAdmin
from .admins.assertions import AssertionAdmin
from .admins.recipients import RecipientAdmin




class DiplomaDetailInline(admin.TabularInline):
    """
    Django admin of Type of diplomas
    """
    model = DiplomaDetail
    max_num = 2
    readonly_fields = [
        'id', 'created'  
    ]
    fields = [
        'id', 'diploma_detail', 'criteria', 'created'         
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()


class DiplomaAdmin(admin.ModelAdmin, CSSAdminMixin):
    """
    Django admin of diploma
    """
    inlines = [DiplomaDetailInline]
    list_display = [
        'thumbnail', 'name', 'diploma_type', 'issuer', 'location',  
        'created', 'created_by'
    ] 
    list_display_links = [
        'thumbnail', 'name',
    ] 
    list_filter = [
        'issuer__name', 'diploma_type', 'created', 
    ]
    search_fields = [
        'name', 'location'
    ]
    readonly_fields = [
        'slug', 'thumbnail', 'linkedin_thumb', 'created', 'created_by',
        'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Diploma's details", {
            'fields': ('issuer', ('name', 'slug'), ('diploma_type', 'tags'), 'url', 'description', 
                         'location')
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

    def thumbnail(self, obj):
        """ Get the diplomas's thumbnail in the admin """

        if obj.img_badge_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.img_badge_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/static/not-available.png" width="75" height="75" >'
            )

    def linkedin_thumb(self, obj):
        """ Get the diploma's thumbnail for linkedin in the admin """

        if obj.img_badge_in_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.img_badge_in_thumb.url.split('/media/')[-1])
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


class AssertionInline(admin.TabularInline):
    """
    Django admin of Assertion
    """
    model = Assertion
    max_num = 0
    readonly_fields = [
        'id', 'email', 'issued_on', 'sent', 'created', 'created_by'
    ]
    fields = [
        'id', 'email', 'issued_on', 'sent', 'created', 'created_by',         
    ]

    def email(self, obj):
        return obj.recipient.email

    def slug(self, obj):
        return obj.user.slug

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()


class DiplomaDetailAdmin(admin.ModelAdmin, CSSAdminMixin):
    """
    Django admin of diploma's detail
    """
    inlines = [AssertionInline]
    list_display = [
        'id', 'thumbnail', 'diploma_detail', 'diploma', 'issuer',     
        'created', 'created_by'
    ] 
    list_display_links = [
        'thumbnail', 'id'
    ] 
    list_filter = [
        'diploma__name', 'diploma__issuer__name', 'diploma_detail', 'created', 
    ]
    search_fields = [
        'diploma__name', 'diploma__issuer__name', 
    ]
    readonly_fields = [
        'id', 'thumbnail', 'diploma', 'issuer', 'diploma_detail', 'criteria',
        'created', 'created_by', 'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Diploma", {
            'fields': (('diploma', 'issuer'), 'thumbnail')
        }),
        ("Diploma's details", {
            'fields': (('diploma_detail', 'id'), 'criteria',)
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': (('created', 'created_by'), ('modified', 'modified_by'))
        }),
    ]

    def issuer(self, obj):
        return obj.diploma.issuer

    def thumbnail(self, obj):
        """ Get the diplomas's thumbnail in the admin """

        if obj.diploma.img_badge_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.diploma.img_badge_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/static/not-available.png" width="75" height="75" >'
            )
    
    def has_add_permission(self, request, obj=None):
        return False













#Admin by defaul 
""" admin.site.register(Assertion, AssertionAdmin)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Diploma, DiplomaAdmin)
admin.site.register(Issuer, IssuerAdmin) """

#Diplofy's admin customed
diplofy_admin_site = DiplofyAdminSite(name='diplofy_admin')

diplofy_admin_site.register(Assertion, AssertionAdmin)
diplofy_admin_site.register(Recipient, RecipientAdmin)
diplofy_admin_site.register(Tag, TagAdmin)
diplofy_admin_site.register(Diploma, DiplomaAdmin)
diplofy_admin_site.register(DiplomaDetail, DiplomaDetailAdmin)
diplofy_admin_site.register(Issuer, IssuerAdmin)