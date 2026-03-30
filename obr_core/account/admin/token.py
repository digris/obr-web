from django.contrib import admin

import unfold.admin
import unfold.decorators
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import TokenProxy

admin.site.unregister(TokenProxy)


@admin.register(TokenProxy)
class CustomTokenAdmin(TokenAdmin, unfold.admin.BaseModelAdmin):
    list_display = [
        "key_display",
        "user",
        "created",
    ]
    fields = [
        "key",
        "user",
    ]
    readonly_fields = [
        "key",
    ]
    search_fields = [
        "key",
        "user__uid",
        "user__email",
    ]
    raw_id_fields = [
        "user",
    ]
    autocomplete_fields = [
        "user",
    ]

    @unfold.decorators.display(
        description="key",
        ordering="key",
        label=True,
    )
    def key_display(self, obj):
        return obj.key
