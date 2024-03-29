from django.contrib import admin

from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import TokenProxy

admin.site.unregister(TokenProxy)


@admin.register(TokenProxy)
class CustomTokenAdmin(TokenAdmin):
    raw_id_fields = [
        "user",
    ]
    fields = [
        "user",
        "key",
    ]
    readonly_fields = [
        "key",
    ]
    search_fields = [
        "key",
        "user__uid",
        "user__email",
    ]
