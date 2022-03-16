from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from social_django.models import UserSocialAuth

from subscription.models import Subscription
from .forms import UserCreationForm, UserChangeForm
from .models import User, Settings, Address, LoginToken
from .email_login import send_login_email


@admin.action(description="Send login e-mail")
# pylint: disable=unused-argument
def send_login_email_action(modeladmin, request, queryset):
    for instance in queryset:
        send_login_email(instance.email)


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


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = [
        "user",
        "line_1",
        "line_2",
        "postal_code",
        "city",
        "country",
    ]
    search_fields = [
        "user__uid",
        "user__email",
        "user__first_name",
        "user__last_name",
        "line_1",
        "line_2",
        "postal_code",
        "city",
        "country",
    ]
    # list_filter = [
    #     "country",
    # ]
    readonly_fields = [
        "user",
    ]


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        "email",
        "uid",
        "phone",
        "migration_source",
        "is_active",
        "is_staff",
        "is_superuser",
        # "date_joined",
        # "last_login",
    ]
    list_filter = [
        "is_staff",
        "is_active",
        "is_superuser",
        "migration_source",
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
    actions = [
        send_login_email_action,
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "phone",
                    "password",
                ),
            },
        ),
        (
            "User Details",
            {
                "fields": (
                    "gender",
                    "first_name",
                    "last_name",
                    "date_of_birth",
                ),
            },
        ),
        (
            "Migration / remote",
            {
                "fields": (
                    "obp_id",
                    "migration_source",
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
