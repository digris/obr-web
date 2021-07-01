# -*- coding: utf-8 -*-
from django.contrib import admin

from identifier.admin import IdentifierInline
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image
from .models import Emission, Editor, EditorImage


class EditorImageInline(SortableImageInlineMixin, admin.TabularInline):
    model = EditorImage


@admin.register(Emission)
class EmissionAdmin(admin.ModelAdmin):
    save_on_top = True
    date_hierarchy = "time_start"
    list_display = [
        "__str__",
        "uid",
        "time_start",
        "time_end",
        "duration",
        "is_current",
    ]
    list_filter = [
        "time_start",
    ]
    search_fields = [
        "uuid",
    ]
    raw_id_fields = [
        "playlist",
    ]

    def is_current(self, obj):
        return obj.is_current

    is_current.boolean = True


@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "image_display",
        "display_name",
        "uid",
        "updated",
        "sync_state",
    ]
    list_filter = [
        "updated",
        "sync_state",
    ]
    search_fields = [
        "display_name",
        "uid",
    ]
    readonly_fields = [
        "uuid",
        "uid",
        "tags",
    ]
    date_hierarchy = "created"
    inlines = [
        EditorImageInline,
        IdentifierInline,
    ]
    raw_id_fields = [
        "user",
    ]

    @admin.display(
        description="Image",
    )
    def image_display(self, obj):
        return get_admin_inline_image(obj)
