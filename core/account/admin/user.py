from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.template.response import TemplateResponse
from django.urls import path
from social_django.models import UserSocialAuth

from subscription.models import Subscription
from sync.admin import sync_qs_action
from ..forms import UserCreationForm, UserChangeForm
from ..models import User, Settings, Address, LoginToken


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

    def get_urls(self):
        urls = super().get_urls()
        user_urls = [
            path("migrate/", self.admin_site.admin_view(self.migrate_user_view)),
        ]
        return user_urls + urls

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
        "sync_state",
    ]
    list_filter = [
        "is_staff",
        "is_active",
        "is_superuser",
        "migration_source",
        "date_joined",
        "last_login",
        "sync_state",
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
        sync_qs_action,
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

    def migrate_user_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
        )
        return TemplateResponse(
            request,
            "admin/account/user/migrate-user.html",
            context,
        )


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