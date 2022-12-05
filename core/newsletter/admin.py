from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import Newsletter, Subscription


@admin.register(Newsletter)
class NewsletterAdmin(
    TranslationAdmin,
):
    save_on_top = True
    list_display = [
        "__str__",
        "description",
        "uid",
    ]
    search_fields = [
        "title",
    ]
    list_filter = [
        "created",
        "updated",
    ]


@admin.register(Subscription)
class SubscriptionAdmin(
    admin.ModelAdmin,
):
    save_on_top = True
    list_display = [
        "newsletter",
        "user",
        "uid",
        "created",
    ]
    raw_id_fields = [
        "user",
    ]
    date_hierarchy = "created"
    search_fields = [
        "user__uid",
        "user__email",
    ]
    list_filter = [
        "newsletter",
        "created",
        "updated",
    ]
