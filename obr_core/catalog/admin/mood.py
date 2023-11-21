from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

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
