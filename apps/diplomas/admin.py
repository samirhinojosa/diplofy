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


class TagAdmin(admin.ModelAdmin, CSSAdminMixin):
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


class RecipientAdmin(ImportMixin, admin.ModelAdmin, CSSAdminMixin):
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
            'fields': (('first_name', 'last_name'), ('email', 'telephone'))
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


class AssertionAdmin(ImportMixin, FilterUserAdmin, CSSAdminMixin):
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
        'id', 'licence', 'email', 'diploma', 'diploma_detail', 'image', 'issuer', 'get_issuer_thumbnail', 'short_url', 'sent', 
        'created', 'created_by', 'modified', 'modified_by'
    ] 
    fieldsets  = [
        ("Diploma", {
            'fields': (('diploma', 'issuer'), ('image', 'diploma_detail'))
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
    
    def diploma(self, obj):
        return obj.diploma_detail.diploma.name
    
    def issuer(self, obj):
        return obj.diploma_detail.diploma.issuer

    def slug(self, obj):
        return obj.user.slug

    def image(self, obj):
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