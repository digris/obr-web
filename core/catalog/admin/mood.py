from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from modeltranslation.admin import TranslationAdmin
from django_json_widget.widgets import JSONEditorWidget
from tagging.models import TaggedItem
from catalog.models.mood import Mood


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
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget(height=500)},
    }
