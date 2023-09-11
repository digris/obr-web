from django.contrib import admin
from django.utils.html import mark_safe

from stats.models import PlayerEvent, StreamEvent
from ua_parser import user_agent_parser
from user_identity.admin import get_admin_link_for_user_identity


@admin.register(PlayerEvent)
class PlayerEventAdmin(
    admin.ModelAdmin,
):
    list_display = [
        "user_identity",
        "user_display",
        "state",
        "duration_display",
        "obj_key",
        "source",
        # "user_identity",
        "device_key",
    ]
    list_filter = [
        "source",
        "time",
        "state",
        "ingested",
    ]
    ordering = ["-time"]
    date_hierarchy = "time"
    search_fields = [
        "obj_key",
        "user_identity",
        "device_key",
    ]

    @admin.display(description="User")
    def user_display(self, obj):
        return get_admin_link_for_user_identity(obj.user_identity)

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
        "user_agent_display",
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

    @admin.display(description="UA")
    def user_agent_display(self, obj):
        parsed = user_agent_parser.Parse(obj.user_agent)
        if parsed.get("user_agent", {}).get("family") == "Other":
            return obj.user_agent[:40]
        html = """
        <div>{browser} {browser_version}<div>
        <dim>{brand} {os} {os_version}<dim>
        """.format(
            browser=parsed.get("user_agent", {}).get("family", "-") or "-",
            browser_version=parsed.get("user_agent", {}).get("major", "-") or "-",
            os=parsed.get("os", {}).get("family", "-") or "-",
            os_version=parsed.get("os", {}).get("major", "-") or "",
            brand=parsed.get("device", {}).get("family", "-") or "-",
        )
        return mark_safe(html)
