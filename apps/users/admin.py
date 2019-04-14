from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from apps.diplomas.admin import diplofy_admin_site


class CustomUserAdmin(UserAdmin):
    """
    customizing authentication user 
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'is_staff'
    ]


admin.site.register(CustomUser, CustomUserAdmin)

#Diplofy's admin customed
diplofy_admin_site.register(CustomUser, CustomUserAdmin)
