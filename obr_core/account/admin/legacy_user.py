from django.contrib import admin

from ..models import LegacyUser


@admin.register(LegacyUser)
class LegacyUserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "user",
        "obp_id",
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
        "first_name",
        "last_name",
        "phone",
        "year_of_birth",
        "gender",
        "date_joined",
        "date_last_login",
    ]
    search_fields = [
        "email",
        "obp_id",
    ]
    list_filter = [
        "date_joined",
        "date_last_login",
        "year_of_birth",
        "gender",
    ]
    date_hierarchy = "date_last_login"
