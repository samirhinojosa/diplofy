from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Added creation of the user's form.
    """
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'email']

class CustomUserChangeForm(UserChangeForm):
    """
    Added updating of the user's form.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email']