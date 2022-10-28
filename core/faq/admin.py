from django.contrib import admin

from modeltranslation.admin import TranslationAdmin
from .models import Category, Topic


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    save_on_top = True
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
class TopicAdmin(TranslationAdmin):
    save_on_top = True
    list_display = [
        "__str__",
        "priority",
        "category",
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
