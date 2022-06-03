from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy
from rest_framework.authtoken.admin import TokenAdmin

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
    search_fields = [
        "key",
        "user__uid",
        "user__email",
    ]
