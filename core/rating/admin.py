from django.contrib import admin

from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    date_hierarchy = "updated"
    list_display = [
        "__str__",
        "user",
        "value",
        "content_type",
        "content_object",
        # "created",
        "updated",
    ]
    list_filter = [
        "value",
    ]
    search_fields = [
        "user__uid",
        "user__email",
    ]
    raw_id_fields = [
        "user",
    ]
