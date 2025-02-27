from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.safestring import mark_safe

import unfold.admin
import unfold.decorators
from catalog.models.mood import Mood
from modeltranslation.admin import TabbedTranslationAdmin
from tagging.models import TaggedItem


class TaggedItemInline(unfold.admin.TabularInline, GenericTabularInline):
    model = TaggedItem
    extra = 0
    autocomplete_fields = [
        "tag",
    ]
    hide_title = True


@admin.register(Mood)
class MoodAdmin(unfold.admin.ModelAdmin, TabbedTranslationAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth = True
    list_filter_sheet = True

    list_display = [
        "mood_display",
        "tags_display",
        "color_display",
        "uid_display",
    ]
    search_fields = [
        "name",
        "uid",
    ]
    list_filter = [
        # "tags",
    ]
    readonly_fields = [
        "uuid",
        "uid",
        "tags",
    ]
    inlines = [
        TaggedItemInline,
    ]

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="mood",
        header=True,
        ordering="name",
    )
    def mood_display(self, obj):
        return obj.name, obj.teaser or "-"

    @unfold.decorators.display(
        description="tags",
        label=True,
    )
    def tags_display(self, obj):
        return [str(t) for t in obj.tags.all()]

    @admin.display(
        description="Color",
        empty_value="-",
    )
    def color_display(self, obj):
        if not obj.rgb:
            return None

        c0 = " ".join([str(b) for b in obj.rgb])
        style = f"background: rgb({c0}); width:40px; height:40px;"
        return mark_safe(f'<div style="{style}"></div>')  # NOQA: S308

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid
