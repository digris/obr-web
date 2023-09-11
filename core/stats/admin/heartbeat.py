from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

from stats.models import Heartbeat
from user_identity.admin import get_admin_link_for_user_identity

IS_ONLINE_THRESHOLD = 120


class IsOnlineFilter(admin.DateFieldListFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        now = timezone.now()
        now.replace(hour=0, minute=0, second=0, microsecond=0)

        self.links = (
            ("All", {}),
            (
                "Online",
                {
                    self.lookup_kwarg_since: str(
                        now - timedelta(seconds=IS_ONLINE_THRESHOLD),
                    ),
                },
            ),
            (
                "Offline",
                {
                    self.lookup_kwarg_until: str(
                        now - timedelta(seconds=IS_ONLINE_THRESHOLD + 1),
                    ),
                },
            ),
        )


@admin.register(Heartbeat)
class HeartbeatAdmin(
    admin.ModelAdmin,
):
    list_display = [
        "user_identity",
        "user_display",
        "time_since_last_heartbeat_in_seconds",
        # "time_since_last_heartbeat",
        "player_source",
        "player_state",
        "user_agent_display",
        "in_foreground",
        "is_online_display",
    ]
    list_filter = [
        ("time", IsOnlineFilter),
        "in_foreground",
    ]
    date_hierarchy = "time"
    search_fields = [
        "user_identity",
    ]
    readonly_fields = [
        "time",
        "user_identity",
        "device_key",
        "user_agent",
        "in_foreground",
        "player_source",
        "player_state",
    ]

    @admin.display(description="Online", boolean=True)
    def is_online_display(self, obj):
        return obj.time_since_last_heartbeat.total_seconds() < IS_ONLINE_THRESHOLD

    @admin.display(description="Last beat [s]")
    def time_since_last_heartbeat_in_seconds(self, obj):
        return round(obj.time_since_last_heartbeat.total_seconds())

    @admin.display(description="User")
    def user_display(self, obj):
        return get_admin_link_for_user_identity(obj.user_identity)

    @admin.display(description="UA")
    def user_agent_display(self, obj):
        return obj.user_agent.split("(")[0].strip()
