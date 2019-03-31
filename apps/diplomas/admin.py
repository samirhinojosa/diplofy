from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Issuer


class IssuerAdmin(admin.ModelAdmin):
    """
    Django admin of Issuers
    """
    list_display = [
        'get_thumbnail_post', 'name', 'slug', 'created', 'created_by',
        'modified', 'modified_by'
    ] 
    list_display_links = [
        'get_thumbnail_post', 'name', 'slug'
    ] 
    readonly_fields = [
        'get_thumbnail_post', 'slug', 'created', 'created_by',
        'modified', 'modified_by'
    ]
    fields = [
        'name', 'slug', 'url', 'telephone', 'description', 
        'image', 'get_thumbnail_post', 'created', 'created_by', 'modified', 'modified_by'
    ]

    def slug(self, obj):
        return obj.user.slug

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()

    #get the issuer's thumbnail in the admin
    def get_thumbnail_post(self, obj):
        if obj.image_thumb:
            return mark_safe(
                '<img src="/media/{url}" >'.format(url = obj.image_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/media/persons/photo/defaultPhoto.jpg" width="150" height="150" >'
            )

    
admin.site.register(Issuer, IssuerAdmin)