from django.contrib import admin

from identifier.admin import IdentifierInline
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image
from modeltranslation.admin import TranslationAdmin
from sync.admin import sync_qs_action

from .models import Editor, EditorImage, Emission


@admin.action(description="Set active")
# pylint: disable=unused-argument
def set_active_action(modeladmin, request, queryset):
    queryset.all().update(is_active=True)


@admin.action(description="Set inactive")
# pylint: disable=unused-argument
def set_inactive_action(modeladmin, request, queryset):
    queryset.all().update(is_active=False)


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

    def is_current(self, obj):  # pragma: no cover
        return obj.is_current

    is_current.boolean = True


@admin.register(Editor)
class EditorAdmin(TranslationAdmin):
    save_on_top = True
    list_display = [
        "image_display",
        "display_name",
        "location",
        "uid",
        # "updated",
        "is_active",
        "sync_state",
    ]
    list_filter = [
        "updated",
        "is_active",
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
    actions = [
        sync_qs_action,
        set_active_action,
        set_inactive_action,
    ]
    raw_id_fields = [
        "user",
    ]

    @admin.display(
        description="Image",
    )
    def image_display(self, obj):  # pragma: no cover
        return get_admin_inline_image(obj.image)
