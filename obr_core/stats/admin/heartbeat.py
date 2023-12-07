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


class DeviceFilter(admin.SimpleListFilter):
    title = "Device"
    parameter_name = "user_agent"

    def lookups(self, request, model_admin):
        return [
            ("web", "Web"),
            ("app", "App"),
        ]

    def queryset(self, request, queryset):
        ua_app = "OBR-App"
        if self.value() == "web":
            return queryset.exclude(
                user_agent__startswith=ua_app,
            )
        if self.value() == "app":
            return queryset.filter(
                user_agent__startswith=ua_app,
            )
        return None


@admin.register(Heartbeat)
class HeartbeatAdmin(
    admin.ModelAdmin,
):
    list_display = [
        "user_identity",
        "user_display",
        "time_since_last_heartbeat_in_seconds",
        "time_online",
        # "created",
        "player_source",
        "player_state",
        "user_agent_display",
        "remote_ip",
        "in_foreground",
        "is_online_display",
    ]
    list_filter = [
        ("time", IsOnlineFilter),
        DeviceFilter,
        "in_foreground",
        "player_source",
        "player_state",
    ]
    date_hierarchy = "time"
    search_fields = [
        "user_identity",
    ]
    readonly_fields = [
        "time",
        "created",
        "user_identity",
        "device_key",
        "user_agent",
        "remote_ip",
        "in_foreground",
        "player_source",
        "player_state",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by("-created")
        return qs

    @admin.display(description="Online", boolean=True)
    def is_online_display(self, obj):
        return obj.time_since_last_heartbeat.total_seconds() < IS_ONLINE_THRESHOLD

    @admin.display(description="Last beat [s]", ordering="time")
    def time_since_last_heartbeat_in_seconds(self, obj):
        return round(obj.time_since_last_heartbeat.total_seconds())

    @admin.display(description="Time online", ordering="created")
    def time_online(self, obj):
        return str(timezone.now() - obj.created).split(".")[0]

    @admin.display(description="User")
    def user_display(self, obj):
        return get_admin_link_for_user_identity(obj.user_identity)

    @admin.display(description="UA")
    def user_agent_display(self, obj):
        return obj.user_agent.split("(")[0].strip()
