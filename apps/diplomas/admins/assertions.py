from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportMixin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields, resources
from apps.df_auth.models import User
from apps.utils.admin import CSSAdminMixin, FilterUserAdmin
from ..models import Assertion, Recipient, Diploma


class AssertionResource(resources.ModelResource):
    """
    Django admin's way to import assertions mass
    """
    recipient = fields.Field(
        column_name = 'recipient',
        attribute = 'recipient',
        widget = ForeignKeyWidget(Recipient, 'email')
    )
    diploma_id = fields.Field(
        column_name = 'diploma_id',
        attribute = 'diploma',
        widget = ForeignKeyWidget(Diploma, 'id')
    )
    created_by = fields.Field(
        column_name = 'created_by',
        attribute = 'created_by',
        widget = ForeignKeyWidget(User, 'username')
    )
    modified_by = fields.Field(
        column_name = 'modified_by',
        attribute = 'modified_by',
        widget = ForeignKeyWidget(User, 'username')
    )
        
    class Meta:
        model = Assertion
        exclude = ('sent')
        fields = ('id', 'recipient', 'diploma_id', 
                    'issued_on', 'expires', 'short_url')
    
    def before_import_row(self, row, **kwargs):
        if row['short_url'] == None:
            row['short_url'] = ' '
        elif row['short_url'] != ' ':
            row['short_url'] = (row['short_url']).strip()

        if not row['id']:
            row['created_by'] = kwargs.get('user')
        else:
            row['modified_by'] = kwargs.get('user')


class AssertionAdmin(ImportMixin, FilterUserAdmin, CSSAdminMixin):
    """
    Django admin of Assertions
    """
    resource_class = AssertionResource
    
    list_display = [
        'recipient', 'licence', 'event', 'diploma', 'issuer', 'issued_on', 'sent', 'created_by'
    ] 
    list_display_links = [
        'licence', 'recipient',
    ]
    list_filter = [
        'diploma__event__issuer__name', 'diploma__event__name', 'sent', 'issued_on', 'created' 
    ]
    search_fields = [
        'diploma__event__issuer__name', 'diploma__event__name', 'recipient__first_name', 'recipient__last_name'
    ]
    readonly_fields = [
        'id', 'licence', 'recipient', 'email', 'event', 'diploma', 'image', 'issuer', 'issuer_image', 'short_url', 'sent', 
        'created', 'created_by', 'modified', 'modified_by'
    ] 
    fieldsets  = [
        ("Diploma", {
            'fields': (('event', 'issuer'), ('image', 'issuer_image'), ('diploma'))
        }),
        ("Assertion's details", {
            'fields': ('licence', ('recipient', 'email'), ('issued_on', 'expires'),
                        ('sent', 'short_url'))
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': (('created', 'created_by'), ('modified', 'modified_by'))
        }),
    ]

    def email(self, obj):
        return obj.recipient.email
    
    def event(self, obj):
        return obj.diploma.event.name
    
    def issuer(self, obj):
        return obj.diploma.event.issuer

    def slug(self, obj):
        return obj.user.slug

    def image(self, obj):
        """ Get the issuer's thumbnail in the admin """

        if obj.diploma.img_badge_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.diploma.img_badge_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/static/not-available.png" width="75" height="75" >'
            )

    def issuer_image(self, obj):
        """ Get the issuer's thumbnail in the admin """

        if obj.diploma.event.issuer.image_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.diploma.event.issuer.image_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/static/not-available.png" width="75" height="75" >'
            )

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()

