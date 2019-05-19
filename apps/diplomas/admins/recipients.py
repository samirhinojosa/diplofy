from django.contrib import admin
from import_export.admin import ImportMixin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields, resources
from apps.df_auth.models import User
from apps.utils.admin import CSSAdminMixin
from ..models import Recipient


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