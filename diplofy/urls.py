"""diplofy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.diplomas.admin import diplofy_admin_site

diplofy_admin_site.site_header = "Diplofy's Admin"
diplofy_admin_site.site_title = "Diplofy's Admin Portal"
diplofy_admin_site.index_title = "Welcome to Diplofy's Portal"

admin.site.site_header = "Diplofy's Admin"
admin.site.site_title = "Diplofy's Admin Portal"
admin.site.index_title = "Welcome to Diplofy's Portal"

urlpatterns = [
    path('my-admin/', admin.site.urls),
    path('myadmin/', diplofy_admin_site.urls),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)