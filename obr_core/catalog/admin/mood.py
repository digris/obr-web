from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.safestring import mark_safe

from catalog.models.mood import Mood
from modeltranslation.admin import TranslationAdmin
from tagging.models import TaggedItem


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 0
    raw_id_fields = [
        "tag",
    ]


@admin.register(Mood)
class MoodAdmin(TranslationAdmin):
    save_on_top = True
    list_display = [
        "__str__",
        "teaser",
        "color_display",
        "tags_display",
        "updated",
    ]
    search_fields = [
        "name",
        "uid",
    ]
    readonly_fields = [
        "uuid",
        "uid",
        "tags",
        # "style",
    ]
    inlines = [
        TaggedItemInline,
    ]

    @admin.display(
        description="Color",
        empty_value="-",
    )
    def color_display(self, obj):
        if not obj.rgb:
            return None

        c0 = " ".join([str(b) for b in obj.rgb])
        style = f"background: rgb({c0}); width:120px; height:40px;"
        return mark_safe(f'<div style="{style}"></div>')  # NOQA: S308

    @admin.display(
        description="Tags",
        empty_value="-",
    )
    def tags_display(self, obj):
        if not obj.tags:
            return None
        return ", ".join([str(t) for t in obj.tags.all()])
