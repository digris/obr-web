from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Identifier


class IdentifierInline(GenericTabularInline):
    model = Identifier
    extra = 0


@admin.register(Identifier)
class IdentifierAdmin(admin.ModelAdmin):
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
