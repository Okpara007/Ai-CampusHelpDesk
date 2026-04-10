from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, RegisterForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ["email", "role", "is_active", "is_staff", "is_superuser"]
    list_filter = ["role", "is_active", "is_staff", "is_superuser"]
    ordering = ["email"]

    fieldsets = UserAdmin.fieldsets + (
        (
            "Helpdesk",
            {
                "fields": ("role", "linked_student"),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Helpdesk",
            {
                "fields": ("email", "role", "linked_student"),
            },
        ),
    )
