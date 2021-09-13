# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from tagging.models import TaggedItem
from catalog.models.mood import Mood


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 0
    raw_id_fields = [
        "tag",
    ]


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
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
    ]
    inlines = [
        TaggedItemInline,
    ]
