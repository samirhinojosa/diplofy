from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.diplomas.admin import diplofy_admin_site
from .forms import UserCreationForm, UserChangeForm
from .models import User, ProxyUser, ProxyGroup


class UserAdmin(UserAdmin):
    """
    customizing authentication user 
    """
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'is_staff'
    ]


#admin.site.register(User, UserAdmin)
admin.site.register(ProxyUser, UserAdmin)

#Diplofy's admin customed
diplofy_admin_site.register(ProxyUser, UserAdmin)
diplofy_admin_site.register(ProxyGroup)