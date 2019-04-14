from django.contrib.admin import AdminSite
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportMixin
from .models import Issuer, Badge, Tag, Recipient, Assertion
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields, resources
from apps.df_auth.models import User


class IssuerAdmin(admin.ModelAdmin):
    """
    Django admin of Issuers
    """
    list_display = [
        'get_thumbnail', 'name', 
        'created', 'created_by', 'modified', 'modified_by'
    ] 
    list_display_links = [
        'get_thumbnail', 'name'
    ] 
    list_filter = [
        'created'
    ]
    search_fields = [
        'name', 'location'
    ]
    readonly_fields = [
        'get_thumbnail', 'slug', 'created', 'created_by', 'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Issuer's details", {
            'fields': ('name', 'slug', 'url', 'telephone', 'description')
        }),
        ("Issuer's image", {
            'fields': ('image', 'get_thumbnail')
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('created', 'created_by', 'modified', 'modified_by')
        }),
    ]

    def get_thumbnail(self, obj):
        """ Get the issuer's thumbnail in the admin """

        if obj.image_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.image_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/media/not-available.png" width="75" height="75" >'
            )

    def slug(self, obj):
        return obj.user.slug

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()


class TagAdmin(admin.ModelAdmin):
    """
    Django admin of Tags
    """
    list_display = [
        'name', 'slug', 'created', 'created_by', 'modified', 'modified_by'
    ] 
    list_display_links = [
        'name', 'slug'
    ] 
    list_filter = [
        'created'
    ]
    search_fields = [
        'name'
    ]
    readonly_fields = [
        'slug', 'created', 'created_by', 'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Tag's details", {
            'fields': ('name', 'slug')
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('created', 'created_by', 'modified', 'modified_by')
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


class BadgeAdmin(admin.ModelAdmin):
    """
    Django admin of bagdes
    """
    inlines = [AssertionInline]
    list_display = [
        'get_thumbnail', 'name', 'id', 'issuer', 'location',  
        'created', 'created_by'
    ] 
    list_display_links = [
        'get_thumbnail', 'name',
    ] 
    list_filter = [
        'issuer', 'tags', 'created'
    ]
    search_fields = [
        'name', 'location'
    ]
    readonly_fields = [
        'id', 'slug', 'get_thumbnail', 'get_linkedin_thumb', 'created', 'created_by',
        'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Badge's details", {
            'fields': ('issuer', 'id', 'name', 'slug', 'url', 'description', 'tags', 'criteria', 
                        'location')
        }),
        ("Badge's main image", {
            'fields': ('image', 'get_thumbnail')
        }),
        ("Badge's image for linkedin", {
            'fields': ('image_linkedin', 'get_linkedin_thumb')
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('created', 'created_by', 'modified', 'modified_by')
        }),
    ]

    def get_thumbnail(self, obj):
        """ Get the issuer's thumbnail in the admin """

        if obj.image_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.image_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/media/not-available.png" width="75" height="75" >'
            )

    def get_linkedin_thumb(self, obj):
        """ Get the badge's thumbnail in the admin """

        if obj.image_linkedin_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.image_linkedin_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/media/not-available.png" width="75" height="75" >'
            )

    def slug(self, obj):
        return obj.user.slug
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()


class RecipientResource(resources.ModelResource):
    """
    Django admin's way to import recipients mass
    """
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
        model = Recipient
        fields = ('id', 'first_name', 'last_name', 'telephone', 'email', 'created_by', 'modified_by')

    def before_import_row(self, row, **kwargs):
        if not row['id']:
            row['created_by'] = kwargs.get('user')
        else:
            row['modified_by'] = kwargs.get('user')


class RecipientAdmin(ImportMixin, admin.ModelAdmin):
    """
    Django admin of Recipient
    """
    resource_class = RecipientResource
    list_display = [
        'email', 'first_name', 'last_name', 'created', 'created_by'
    ] 
    list_display_links = [
        'email'
    ] 
    list_filter = [
        'created' 
    ]
    search_fields = [
        'email', 'first_name', 'last_name',
    ]
    readonly_fields = [
        'created', 'created_by', 'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Recipient's details", {
            'fields': ('first_name', 'last_name', 'telephone', 'email')
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('created', 'created_by', 'modified', 'modified_by')
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
    
    def import_data(self, dataset, dry_run=False, raise_errors=False, 
                    use_transactions=None, collect_failed_rows=False, **kwargs):
        """ Getting the user's request to pass it to the import """

        result = RecipientResource.import_data(dataset, dry_run=False, raise_errors=False, 
                                                use_transactions=None, user=self.request.user)

        return result


class AssertionResource(resources.ModelResource):
    """
    Django admin's way to import assertions mass
    """
    recipient = fields.Field(
        column_name = 'recipient',
        attribute = 'recipient',
        widget = ForeignKeyWidget(Recipient, 'email')
    )
    badge_name = fields.Field(
        column_name = 'badge_name',
        attribute = 'badge',
        widget = ForeignKeyWidget(Badge, 'name')
    )
    badge_id = fields.Field(
        column_name = 'badge_id',
        attribute = 'badge',
        widget = ForeignKeyWidget(Badge, 'id')
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
        fields = ('id', 'recipient', 'recipient', 'badge_name', 'badge_id', 
                    'issued_on', 'expires', 'short_url')
    
    def before_import_row(self, row, **kwargs):
        if not row['id']:
            row['created_by'] = kwargs.get('user')
        else:
            row['modified_by'] = kwargs.get('user')


class AssertionAdmin(ImportMixin, admin.ModelAdmin):
    """
    Django admin of Assertions
    """
    resource_class = AssertionResource
    
    list_display = [
        'licence', 'recipient', 'badge', 'issuer', 'issued_on', 'sent', 
    ] 
    list_display_links = [
        'licence', 'recipient',
    ] 
    list_filter = [
        'badge', 'badge__issuer', 'issued_on', 'created' 
    ]
    search_fields = [
        'recipient'
    ]
    readonly_fields = [
        'id', 'licence', 'email', 'get_badge_thumbnail', 'issuer', 'get_issuer_thumbnail', 'short_url', 'sent', 'created', 'created_by', 'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Assertion's details", {
            'fields': ('id', 'licence', 'recipient', 'email', 'badge', 'get_badge_thumbnail', 'issuer', 'get_issuer_thumbnail', 'issued_on', 'expires',
                        'short_url', 'sent')
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('created', 'created_by', 'modified', 'modified_by')
        }),
    ]

    def email(self, obj):
        return obj.recipient.email
    
    def issuer(self, obj):
        return obj.badge.issuer

    def slug(self, obj):
        return obj.user.slug

    def get_badge_thumbnail(self, obj):
        """ Get the issuer's thumbnail in the admin """

        if obj.badge.image_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.badge.image_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/media/not-available.png" width="75" height="75" >'
            )

    def get_issuer_thumbnail(self, obj):
        """ Get the issuer's thumbnail in the admin """

        if obj.badge.issuer.image_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.badge.issuer.image_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/media/not-available.png" width="75" height="75" >'
            )


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()

    def import_data(self, dataset, dry_run=False, raise_errors=False, 
                    use_transactions=None, collect_failed_rows=False, **kwargs):
        """ Getting the user's request to pass it to the import """

        result = AssertionResource.import_data(dataset, dry_run=False, raise_errors=False, 
                                                use_transactions=None, user=self.request.user)

        return result
        

class DiplofyAdminSite(AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            'Issuers': 1,
            'Tags': 2,
            'Badges': 3,
            'Recipients': 4,
            'Assertions': 5,
            'Contactaus': 6,
            'Interested': 7,
            'Groups': 8,
            'Users': 9
        }
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list

#Admin by defaul 
admin.site.register(Assertion, AssertionAdmin)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Issuer, IssuerAdmin)

#Diplofy's admin customed
diplofy_admin_site = DiplofyAdminSite(name='diplofy_admin')

diplofy_admin_site.register(Assertion, AssertionAdmin)
diplofy_admin_site.register(Recipient, RecipientAdmin)
diplofy_admin_site.register(Tag, TagAdmin)
diplofy_admin_site.register(Badge, BadgeAdmin)
diplofy_admin_site.register(Issuer, IssuerAdmin)