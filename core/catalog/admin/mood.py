# -*- coding: utf-8 -*-
from django.contrib import admin

from catalog.models.mood import Mood


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
    ]
