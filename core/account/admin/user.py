from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.template.response import TemplateResponse
from django.urls import path

from social_django.models import UserSocialAuth
from subscription.models import Subscription
from sync.admin import sync_qs_action

from ..forms import UserChangeForm, UserCreationForm
from ..models import Address, LoginToken, Settings, Theme, User


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

    readonly_fields = [
        "country",
    ]

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
    ]
    # list_filter = [
    #     "country",
    # ]
    readonly_fields = [
        "user",
    ]


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    model = Theme
    list_display = [
        "user",
    ]
    search_fields = [
        "user__uid",
        "user__email",
    ]
    raw_id_fields = [
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
        "country",
        "migration_source",
        "is_active",
        "is_staff",
        "is_superuser",
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
        "sync_last_update",
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
                    "country",
                    "year_of_birth",
                    "favorite_venue",
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
        "uid",
        "first_name",
        "last_name",
        "country",
    ]
    ordering = [
        "-date_joined",
    ]

    def delete_model(self, request, obj):
        # NOTE: to prevent signals from running we perform `_raw_delete` on
        #       ratings / votes

        if obj.rated_items.count():
            # pylint: disable=protected-access
            obj.rated_items.all()._raw_delete(obj.rated_items.db)  # NOQA: SLF001

        return super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        raise Exception("Bulk delete is disabled")

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
