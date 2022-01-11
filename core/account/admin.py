from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from social_django.models import UserSocialAuth

from subscription.models import Subscription
from .forms import UserCreationForm, UserChangeForm
from .models import User, Settings, Address, LoginToken


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


class AddressInline(admin.StackedInline):
    model = Address

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "line_1",
                    "line_2",
                    "postal_code",
                    "city",
                    "country",
                ),
            },
        ),
    )


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        "email",
        "uid",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    list_filter = [
        "is_staff",
        "is_active",
        "is_superuser",
        "date_joined",
        "last_login",
    ]
    readonly_fields = [
        "last_login",
        "date_joined",
        "uuid",
        "uid",
    ]
    date_hierarchy = "date_joined"
    inlines = [
        AddressInline,
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
            "User Details",
            {
                "fields": (
                    "first_name",
                    "last_name",
                ),
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
    search_fields = [
        "email",
        "first_name",
        "last_name",
        "address__country",
    ]
    ordering = [
        "-date_joined",
    ]


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
    def is_valid_display(self, obj):  # pragma: no cover
        return obj.is_valid
