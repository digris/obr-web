from django.contrib import admin
from stats.models import PlayerEvent


@admin.register(PlayerEvent)
class PlayerEventAdmin(admin.ModelAdmin):
    list_display = [
        "time",
        "state",
        "duration_display",
        "obj_key",
        "source",
        "user_identity",
        # "device_key",
    ]
    list_filter = [
        "time",
        "state",
        "ingested",
    ]
    date_hierarchy = "time"
    search_fields = [
        "obj_key",
        "user_identity",
        "device_key",
    ]

    @admin.display(description="Duration")
    def duration_display(self, obj):
        return obj.duration
