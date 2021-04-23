from django.contrib import admin

from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "user",
        "value",
        "content_type",
        "content_object",
    ]

    list_filter = [
        "value",
    ]
