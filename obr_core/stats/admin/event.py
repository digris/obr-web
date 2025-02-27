from django.contrib import admin
from django.utils import timezone
from django.utils.html import mark_safe

import unfold.admin
import unfold.decorators
from stats.models import PlayerEvent, StreamEvent
from ua_parser import user_agent_parser
from user_identity.admin import get_admin_link_for_user_identity


@admin.register(PlayerEvent)
class PlayerEventAdmin(
    unfold.admin.ModelAdmin,
):
    list_display = [
        "state_display",
        "time_display",
        "time_end_display",
        #
        "calculated_duration_s",
        #
        "max_duration_display",
        # "annotated_duration_display",
        "obj_key",
        "source",
        "user_display",
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
    exclude = [
        "time",
        "time_end",
    ]
    readonly_fields = [
        "time_display",
        "time_end_display",
        "state",
        "source",
        "obj_key",
        "user_identity",
        "device_key",
        "max_duration",
        #
        "calculated_duration_s",
        "duration_display",
    ]

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="state",
        label={
            "playing": "success",
            "paused": "info",
        },
    )
    def state_display(self, obj):
        return obj.state

    @admin.display(description="Time", ordering="time")
    def time_display(self, obj):
        timestamp_in_tz = obj.time.astimezone(timezone.get_default_timezone())
        return timestamp_in_tz.strftime("%Y-%m-%d %H:%M:%S")

    @admin.display(description="Time end")
    def time_end_display(self, obj):
        if not obj.time_end:
            return None
        timestamp_in_tz = obj.time_end.astimezone(timezone.get_default_timezone())
        return timestamp_in_tz.strftime("%H:%M:%S")

    @admin.display(description="Duration (est)")
    def annotated_duration_display(self, obj):
        return "N/A"
        # if obj.state == PlayerEvent.State.STOPPED:
        # if not obj.annotated_duration:

    @admin.display(description="Duration")
    def duration_display(self, obj):
        if not obj.time_end:
            return None
        return round((obj.time_end - obj.time).total_seconds(), 3)

    @admin.display(description="Duration (max)")
    def max_duration_display(self, obj):
        if not obj.max_duration:
            return None
        return round(obj.max_duration.total_seconds())

    @admin.display(description="User")
    def user_display(self, obj):
        return get_admin_link_for_user_identity(obj.user_identity)


@admin.register(StreamEvent)
class StreamEventAdmin(
    unfold.admin.ModelAdmin,
):
    list_display = [
        "time_start",
        "seconds_connected",
        "origin_display",
        "ip",
        "method",
        "status",
        "path",
        "bytes_sent",
        "referer",
        "user_agent_display",
        "geoip_country",
        "geoip_region",
        "geoip_city",
    ]
    list_filter = [
        "origin",
        "time_start",
        "time_end",
        "path",
        "geoip_country",
    ]
    date_hierarchy = "time_start"
    search_fields = [
        "ip",
        "path",
        "referer",
        "user_agent",
        "geoip_city",
        "geoip_region",
    ]
    readonly_fields = [
        "device_key",
        "geoip_city",
        "geoip_region",
        "geoip_country",
    ]

    def has_change_permission(self, request, obj=None):
        return False

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="origin",
        label=True,
    )
    def origin_display(self, obj):
        return obj.origin

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
