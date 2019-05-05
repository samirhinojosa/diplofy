from django.contrib.admin import AdminSite
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportMixin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields, resources
from apps.df_auth.models import User
from apps.utils.admin import FilterUserAdmin
from .models import Issuer, Diploma, DiplomaDetail, Tag, Recipient, Assertion

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
        'created_by', 'created'
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
            'fields': (('created', 'created_by'), ('modified', 'modified_by'))
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
        'created_by', 'created'
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


class DiplomaAdmin(admin.ModelAdmin):
    """
    Django admin of diploma
    """
    inlines = [DiplomaDetailInline]
    list_display = [
        'get_thumbnail', 'name', 'diploma_type', 'issuer', 'location',  
        'created', 'created_by'
    ] 
    list_display_links = [
        'get_thumbnail', 'name',
    ] 
    list_filter = [
        'issuer__name', 'diploma_type', 'created', 
    ]
    search_fields = [
        'name', 'location'
    ]
    readonly_fields = [
        'slug', 'get_thumbnail', 'get_linkedin_thumb', 'created', 'created_by',
        'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Diploma's details", {
            'fields': ('issuer', 'name', 'diploma_type', 'slug', 'url', 'description', 
                        'tags', 'location')
        }),
        ("Diploma's main image", {
            'fields': ('img_badge', 'get_thumbnail')
        }),
        ("Diploma's image for linkedin", {
            'fields': ('img_badge_in', 'get_linkedin_thumb')
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('created', 'created_by', 'modified', 'modified_by')
        }),
    ]

    def get_thumbnail(self, obj):
        """ Get the diplomas's thumbnail in the admin """

        if obj.img_badge_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.img_badge_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/static/not-available.png" width="75" height="75" >'
            )

    def get_linkedin_thumb(self, obj):
        """ Get the diploma's thumbnail for linkedin in the admin """

        if obj.img_badge_in_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.img_badge_in_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/static_files/not-available.png" width="75" height="75" >'
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


class DiplomaDetailAdmin(admin.ModelAdmin):
    """
    Django admin of diploma's detail
    """
    inlines = [AssertionInline]
    list_display = [
        'id', 'get_thumbnail', 'diploma_detail', 'diploma', 'issuer',     
        'created', 'created_by'
    ] 
    list_display_links = [
        'get_thumbnail', 'id'
    ] 
    list_filter = [
        'diploma__name', 'diploma__issuer__name', 'diploma_detail', 'created', 
    ]
    search_fields = [
        'diploma__name', 'diploma__issuer__name', 
    ]
    readonly_fields = [
        'id', 'get_thumbnail', 'diploma', 'issuer', 'diploma_detail', 'criteria',
        'created', 'created_by', 'modified', 'modified_by'
    ]
    fieldsets  = [
        ("Diploma", {
            'fields': ('get_thumbnail', 'diploma', 'issuer',)
        }),
        ("Diploma's details", {
            'fields': ('id', 'diploma_detail', 'criteria',)
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('created', 'created_by', 'modified', 'modified_by')
        }),
    ]

    def issuer(self, obj):
        return obj.diploma.issuer

    def get_thumbnail(self, obj):
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
        row['first_name'] = (row['first_name'].title()).strip()
        row['last_name'] = (row['last_name'].title()).strip()
        row['email'] = (row['email'].lower()).strip()


        if row['telephone'] == None:
            row['telephone'] = ' '
        elif row['telephone'] != ' ':
            row['telephone'] = (row['telephone']).strip()

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
    diploma_id = fields.Field(
        column_name = 'diploma_id',
        attribute = 'diploma_detail',
        widget = ForeignKeyWidget(DiplomaDetail, 'id')
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
        fields = ('id', 'recipient', 'recipient', 'diploma_id', 
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


class AssertionAdmin(ImportMixin, FilterUserAdmin):
    """
    Django admin of Assertions
    """
    resource_class = AssertionResource
    
    list_display = [
        'licence', 'recipient', 'diploma', 'diploma_detail', 'issuer', 'issued_on', 'sent', 
    ] 
    list_display_links = [
        'licence', 'recipient',
    ]
    list_filter = [
        'diploma_detail__diploma__issuer__name', 'diploma_detail__diploma__name', 'sent', 'issued_on', 'created' 
    ]
    search_fields = [
        'diploma_detail__diploma__issuer__name', 'diploma_detail__diploma__name', 'recipient__first_name', 'recipient__last_name'
    ]
    readonly_fields = [
        'id', 'licence', 'email', 'diploma', 'diploma_detail', 'diploma_image', 'issuer', 'get_issuer_thumbnail', 'short_url', 'sent', 
        'created', 'created_by', 'modified', 'modified_by'
    ] 
    fieldsets  = [
        ("Diploma", {
            'fields': ('issuer', 'diploma', 'diploma_image', 'diploma_detail',)
        }),
        ("Assertion's details", {
            'fields': ('licence', 'recipient', 'email', 'issued_on', 'expires',
                        'short_url', 'sent')
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('created', 'created_by', 'modified', 'modified_by')
        }),
    ]

    def email(self, obj):
        return obj.recipient.email
    
    def diploma(self, obj):
        return obj.diploma_detail.diploma.name
    
    def issuer(self, obj):
        return obj.diploma_detail.diploma.issuer

    def slug(self, obj):
        return obj.user.slug

    def diploma_image(self, obj):
        """ Get the issuer's thumbnail in the admin """

        if obj.diploma_detail.diploma.img_badge_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.diploma_detail.diploma.img_badge_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/media/not-available.png" width="75" height="75" >'
            )

    def get_issuer_thumbnail(self, obj):
        """ Get the issuer's thumbnail in the admin """

        if obj.diploma_detail.diploma.issuer.image_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.diploma_detail.diploma.issuer.image_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/media/not-available.png" width="75" height="75" >'
            )

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()


class DiplofyAdminSite(AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            'Issuers': 1,
            'Tags': 2,
            'Diplomas': 3,
            'Types of Diplomas': 4,
            'Recipients': 5,
            'Assertions': 6,
            'Contactaus': 7,
            'Interested': 8,
            'Groups': 9,
            'Users': 10
        }
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list



#Admin by defaul 
#admin.site.register(Assertion, AssertionAdmin)
#admin.site.register(Recipient, RecipientAdmin)
#admin.site.register(Tag, TagAdmin)
#admin.site.register(Diploma, DiplomaAdmin)
#admin.site.register(Issuer, IssuerAdmin)

#Diplofy's admin customed
diplofy_admin_site = DiplofyAdminSite(name='diplofy_admin')

diplofy_admin_site.register(Assertion, AssertionAdmin)
diplofy_admin_site.register(Recipient, RecipientAdmin)
diplofy_admin_site.register(Tag, TagAdmin)
diplofy_admin_site.register(Diploma, DiplomaAdmin)
diplofy_admin_site.register(DiplomaDetail, DiplomaDetailAdmin)
diplofy_admin_site.register(Issuer, IssuerAdmin)