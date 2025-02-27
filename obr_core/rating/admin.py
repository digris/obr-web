from django.contrib import admin

import unfold.admin
import unfold.decorators

from .models import Vote


@admin.register(Vote)
class VoteAdmin(
    unfold.admin.ModelAdmin,
):
    compressed_fields = True

    date_hierarchy = "updated"
    list_display = [
        # "__str__",
        "content_object",
        "user",
        "value",
        "source",
        "scope",
        "content_type",
        # "content_object",
        "created",
        "comment",
    ]
    list_filter = [
        "value",
        "source",
        "scope",
        "updated",
    ]
    search_fields = [
        "user__uid",
        "user__email",
    ]
    autocomplete_fields = [
        "user",
    ]
    readonly_fields = [
        "created",
        "updated",
    ]
