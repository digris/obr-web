# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from social_django.admin import UserSocialAuth

from .forms import UserCreationForm, UserChangeForm
from .models import User, Settings


class UserSocialAuthInline(admin.TabularInline):
    model = UserSocialAuth
    extra = 0
    readonly_fields = [
        "provider",
        "uid",
    ]
    exclude = [
        "extra_data",
    ]


class SettingsInline(admin.TabularInline):
    model = Settings
    can_delete = False


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
        "signup_completed",
    ]
    list_filter = [
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
        "signup_completed",
    ]
    readonly_fields = [
        "last_login",
        "date_joined",
    ]
    inlines = [
        SettingsInline,
        UserSocialAuthInline,
    ]
    fieldsets = (
        (
            None,
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "signup_completed",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "signup_completed",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
