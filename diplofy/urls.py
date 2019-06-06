from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.diplomas.admin import diplofy_admin_site

diplofy_admin_site.site_header = "Diplofy's Admin"
diplofy_admin_site.site_title = "Diplofy's Admin Portal"
diplofy_admin_site.index_title = "Welcome to Diplofy's Portal"

urlpatterns = [
    path('', include('apps.diplomas.urls')),
    path('myadmin/', diplofy_admin_site.urls),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)