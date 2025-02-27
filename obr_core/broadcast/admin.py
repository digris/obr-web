from django.contrib import admin
from django.utils import timezone

import unfold.admin
import unfold.contrib.filters.admin
import unfold.decorators
from identifier.admin import IdentifierInline
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image
from modeltranslation.admin import TabbedTranslationAdmin
from sync.admin import SyncAdminMixin, sync_qs_action

from .models import Editor, EditorImage, Emission


@admin.action(description="Set active")
# pylint: disable=unused-argument
def set_active_action(modeladmin, request, queryset):
    queryset.all().update(is_active=True)


@admin.action(description="Set inactive")
# pylint: disable=unused-argument
def set_inactive_action(modeladmin, request, queryset):
    queryset.all().update(is_active=False)


class EditorImageInline(SortableImageInlineMixin, unfold.admin.TabularInline):
    model = EditorImage


@admin.register(Emission)
class EmissionAdmin(unfold.admin.ModelAdmin):
    compressed_fields = True
    list_filter_sheet = False

    date_hierarchy = "time_start"
    list_display = [
        "emission_display",
        "duration",
        "state_display",
        "time_start",
        "time_end",
    ]
    list_filter = [
        "time_start",
    ]
    search_fields = [
        "uuid",
    ]
    autocomplete_fields = [
        "playlist",
    ]

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="emission",
        header=True,
        ordering="name",
    )
    def emission_display(self, obj):
        if not obj.playlist:
            return ["-"]
        return obj.playlist, obj.playlist.name

    @unfold.decorators.display(
        description="state",
        label={
            "upcoming": "info",
            "current": "success",
            "past": "-",
        },
    )
    def state_display(self, obj):
        if obj.is_current:
            return "current"
        now = timezone.now()
        if obj.time_start > now:
            return "upcoming"
        return "past"

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid


@admin.register(Editor)
class EditorAdmin(SyncAdminMixin, unfold.admin.ModelAdmin, TabbedTranslationAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth = True
    list_filter_sheet = False

    date_hierarchy = "created"
    list_display = [
        "image_display",
        "editor_display",
        "is_active_display",
        "sync_last_update",
        "sync_state_display",
        "uid_display",
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

    ###################################################################
    # display
    ###################################################################
    @admin.display(
        description="Image",
    )
    def image_display(self, obj):  # pragma: no cover
        return get_admin_inline_image(obj.image)

    @unfold.decorators.display(
        description="editor",
        header=True,
        ordering="name",
    )
    def editor_display(self, obj):
        return obj.display_name, obj.location or "-"

    @unfold.decorators.display(
        description="active",
        ordering="is_active",
        label={
            "active": "success",
            "inactive": "-",
        },
    )
    def is_active_display(self, obj):
        return "active" if obj.is_active else "inactive"

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid
