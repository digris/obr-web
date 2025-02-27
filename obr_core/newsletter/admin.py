from django.contrib import admin

import unfold.admin
import unfold.decorators
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Newsletter, Subscription


@admin.register(Newsletter)
class NewsletterAdmin(
    unfold.admin.ModelAdmin,
    TabbedTranslationAdmin,
):
    save_on_top = True
    list_display = [
        "__str__",
        "description",
        "mailchimp_tag",
        "uid_display",
    ]
    search_fields = [
        "title",
    ]
    list_filter = [
        "created",
        "updated",
    ]

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid


@admin.register(Subscription)
class SubscriptionAdmin(
    unfold.admin.ModelAdmin,
):
    save_on_top = True
    list_display = [
        "user",
        "newsletter",
        "mailchimp_subscriber_hash",
        "created",
        "uid_display",
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

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid
