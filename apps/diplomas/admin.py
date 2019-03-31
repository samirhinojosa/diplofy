from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Issuer, Badge, Tag, Recipient


class IssuerAdmin(admin.ModelAdmin):
    """
    Django admin of Issuers
    """
    can_delete = False
    list_display = [
        'get_thumbnail', 'name', 
        'created', 'created_by', 'modified', 'modified_by'
    ] 
    list_display_links = [
        'get_thumbnail', 'name'
    ] 
    list_filter = [
        'name'
    ]
    readonly_fields = [
        'get_thumbnail', 'slug', 'created', 'created_by',
        'modified', 'modified_by'
    ]
    fields = [
        'name', 'slug', 'url', 'telephone', 'description', 
        'image', 'get_thumbnail', 'created', 'created_by', 'modified', 'modified_by'
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
    def get_thumbnail(self, obj):
        if obj.image_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.image_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/media/not-available.png" width="75" height="75" >'
            )


class TagAdmin(admin.ModelAdmin):
    """
    Django admin of Tags
    """
    list_display = [
        'name', 'slug', 'created', 'created_by',
        'modified', 'modified_by'
    ] 
    list_display_links = [
        'name', 'slug'
    ] 
    readonly_fields = [
        'slug', 'created', 'created_by', 'modified', 
        'modified_by'
    ]

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
    list_display = [
        'get_thumbnail', 'name', 'issuer', 'location',  
        'created', 'created_by'
    ] 
    list_display_links = [
        'get_thumbnail', 'name',
    ] 
    list_filter = [
        'issuer', 'tags', 'location'
    ]
    readonly_fields = [
        'get_thumbnail', 'slug', 'get_linkedin_thumb', 'created', 'created_by',
        'modified', 'modified_by'
    ]
    fields = [
        'issuer', 'name', 'slug', 'url', 'description', 'tags', 'criteria', 
        'location', 'image', 'get_thumbnail', 'image_linkedin', 'get_linkedin_thumb',
        'created', 'created_by', 'modified', 'modified_by'
    ]

    def slug(self, obj):
        return obj.user.slug

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()

    #get the badge's thumbnail in the admin
    def get_thumbnail(self, obj):
        if obj.image_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.image_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/media/not-available.png" width="75" height="75" >'
            )

    #get the badge's thumbnail in the admin
    def get_linkedin_thumb(self, obj):
        if obj.image_linkedin_thumb:
            return mark_safe(
                '<img src="/media/{url}" width="75" height="75" >'.format(url = obj.image_linkedin_thumb.url.split('/media/')[-1])
            )
        else:
            return mark_safe(
                '<img src="/media/not-available.png" width="75" height="75" >'
            )


class RecipientAdmin(admin.ModelAdmin):
    """
    Django admin of Recipient
    """
    list_display = [
        'email', 'first_name', 'last_name', 'created', 'created_by'
    ] 
    list_display_links = [
        'email'
    ] 
    readonly_fields = [
        'created', 'created_by', 'modified', 'modified_by'
    ]
    fields = [
        'first_name', 'last_name', 'telephone', 'email',
        'created', 'created_by', 'modified', 'modified_by'
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()




admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Issuer, IssuerAdmin)