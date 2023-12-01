from django.contrib import admin

from ..models import LegacyUser


@admin.register(LegacyUser)
class LegacyUserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "user",
        "obp_id",
        "date_joined",
        "date_last_login",
    ]
    readonly_fields = [
        "email",
        "obp_id",
    ]
    search_fields = [
        "email",
        "obp_id",
    ]
    list_filter = [
        "date_joined",
        "date_last_login",
    ]
    date_hierarchy = "date_last_login"
