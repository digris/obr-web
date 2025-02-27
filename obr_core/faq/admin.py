from django.contrib import admin

import unfold.admin
import unfold.decorators
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Category, Topic


@admin.register(Category)
class CategoryAdmin(
    unfold.admin.ModelAdmin,
    TabbedTranslationAdmin,
):
    compressed_fields = False
    warn_unsaved_form = True

    list_display = [
        "__str__",
        "priority",
    ]
    search_fields = [
        "name",
    ]
    list_editable = [
        "priority",
    ]


@admin.register(Topic)
class TopicAdmin(
    unfold.admin.ModelAdmin,
    TabbedTranslationAdmin,
):
    compressed_fields = True
    warn_unsaved_form = True

    list_display = [
        "__str__",
        "category",
        "priority",
    ]
    search_fields = [
        "name",
    ]
    list_filter = [
        "category",
    ]
    list_editable = [
        "priority",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("category", "priority"),
                    "question",
                    "answer",
                ],
            },
        ),
    ]
