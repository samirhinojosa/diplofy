from django.contrib import admin
from apps.df_auth.models import User
from apps.utils.admin import CSSAdminMixin
from ..models import Tag


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