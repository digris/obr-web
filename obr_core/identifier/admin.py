from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

import unfold.admin

from .models import Identifier


class IdentifierInline(unfold.admin.TabularInline, GenericTabularInline):
    model = Identifier
    extra = 0
    tab = True
    hide_title = True


@admin.register(Identifier)
class IdentifierAdmin(unfold.admin.ModelAdmin):
    list_display = [
        "__str__",
        "value",
        "content_type",
    ]

    list_filter = [
        "scope",
    ]

    search_fields = [
        "value",
        "uid",
    ]
