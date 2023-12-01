from django.contrib import admin

from account import email_login

from ..models import LegacyUser


@admin.action(description="Send login email")
# pylint: disable=unused-argument
def send_login_email(modeladmin, request, queryset):
    for legacy_user in queryset.all():
        email_login.send_login_email(email=legacy_user.email)


@admin.register(LegacyUser)
class LegacyUserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "user",
        "obp_id",
        "is_listener",
        "first_name",
        "last_name",
        "phone",
        "year_of_birth",
        "gender",
        "date_joined",
        "date_last_login",
    ]
    readonly_fields = [
        "email",
        "user",
        "obp_id",
        "date_joined",
        "date_last_login",
        "first_name",
        "last_name",
        "phone",
        "year_of_birth",
        "gender",
        "date_joined",
        "date_last_login",
        "is_listener",
    ]
    search_fields = [
        "email",
        "obp_id",
    ]
    list_filter = [
        "is_listener",
        "date_joined",
        "date_last_login",
        "year_of_birth",
        "gender",
    ]
    date_hierarchy = "date_last_login"
    actions = [
        send_login_email,
    ]
