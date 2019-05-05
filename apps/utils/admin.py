from django.contrib import admin

class FilterUserAdmin(admin.ModelAdmin):
    """
    Abstract base class to filter data by user
    """

    class Meta:
        abstract = True

    def get_queryset(self, request): 
        qs = super(FilterUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter()
        else:
            return qs.filter(created_by=request.user)

