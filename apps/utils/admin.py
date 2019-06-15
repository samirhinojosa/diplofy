from django.contrib import admin
from django.conf import settings
from django.apps import apps
from django.contrib.admin import AdminSite
from django.utils.translation import gettext as _
from django.template.response import TemplateResponse


class CSSAdminMixin(object):
    """
    Split admin's forms through CSS
    """
    class Media:
        css = {
            'all': ('css/extra-style.css',),
        }

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


class DiplofyAdminSite(AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: settings.LINKS_ORDERING[x['name']])

        return app_list
    
    def app_index(self, request, app_label, extra_context=None):
        """
        Return a sorted list of all models within each app.
        """
        app_dict = self._build_app_dict(request, app_label)
        
        if not app_dict:
            raise Http404('The requested admin page does not exist.')

        # Sort the models alphabetically within each app.
        app_dict['models'].sort(key=lambda x: settings.LINKS_ORDERING[x['name']])
        app_name = apps.get_app_config(app_label).verbose_name
        context = {
            **self.each_context(request),
            'title': _('%(app)s administration') % {'app': app_name},
            'app_list': [app_dict],
            'app_label': app_label,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context)