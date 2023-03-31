from django.contrib import admin

from stats.models import PlayerEvent, StreamEvent


@admin.register(PlayerEvent)
class PlayerEventAdmin(
    admin.ModelAdmin,
):
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


@admin.register(StreamEvent)
class StreamEventAdmin(
    admin.ModelAdmin,
):
    list_display = [
        "time_start",
        "seconds_connected",
        "ip",
        "method",
        "status",
        "path",
        "bytes_sent",
        "referer",
        "user_agent",
    ]
    list_filter = [
        "time_start",
        "time_end",
        "path",
    ]
    date_hierarchy = "time_start"
    search_fields = [
        "ip",
        "path",
        "referer",
        "user_agent",
    ]

    # @admin.display(description="Time")
    # def time_display(self, obj):
    #     return obj.time_start.strftime("%d-%m-%y %H:%M:%S")
