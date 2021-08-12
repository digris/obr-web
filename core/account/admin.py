# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from social_django.models import UserSocialAuth

from subscription.models import Subscription
from .forms import UserCreationForm, UserChangeForm
from .models import User, Settings, LoginToken


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


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 0


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
        # "is_staff",
        "uid",
        "is_active",
        # "is_superuser",
    ]
    list_filter = [
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
    ]
    readonly_fields = [
        "last_login",
        "date_joined",
        "uuid",
        "uid",
    ]
    inlines = [
        SettingsInline,
        SubscriptionInline,
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
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(LoginToken)
class LoginTokenAdmin(admin.ModelAdmin):

    save_on_top = True
    list_display = [
        "uid",
        "token_display",
        "email",
        "created",
        "claimed",
        "is_valid_display",
    ]
    readonly_fields = [
        "value",
    ]
    date_hierarchy = "created"

    @admin.display(
        boolean=True,
        description="Valid",
    )
    def is_valid_display(self, obj):
        return obj.is_valid
