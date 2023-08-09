from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        "pk",
        "username",
        "password",
        "email",
        "first_name",
        "last_name",
    )
    list_filter = ("username", "email")
    change_password_form = AdminPasswordChangeForm
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
