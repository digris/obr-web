from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

import unfold.admin
import unfold.contrib.inlines.admin
import unfold.decorators
from stats.models import Heartbeat, PlayerEvent
from user_identity.admin import get_admin_link_for_user_identity

IS_ONLINE_THRESHOLD = 120


class PlayerEventInline(
    unfold.contrib.inlines.admin.NonrelatedTabularInline,
):
    model = PlayerEvent
    extra = 0
    hide_title = True

    fieldsets = [
        (
            "",
            {
                "fields": [
                    "time_display",
                    "source",
                    "state",
                    "duration_display",
                    "obj_key",
                ],
            },
        ),
    ]

    readonly_fields = [
        "time_display",
        "duration_display",
    ]

    def get_form_queryset(self, obj):
        qs = self.model.objects.filter(device_key=obj.device_key)
        qs = qs.filter(time__gte=obj.created).exclude(
            state__in=["buffering", "stopped"],
        )
        return qs

    @staticmethod
    def save_new_instance(parent, instance):
        return False

    @staticmethod
    def has_add_permission(request, obj):
        return False

    @staticmethod
    def has_change_permission(request, obj):
        return False

    @staticmethod
    def has_delete_permission(request, obj):
        return False

    @admin.display(description="Time", empty_value="-")
    def time_display(self, obj):
        return f"{obj.time:%H:%M:%S}"

    @admin.display(description="Duration", empty_value="-")
    def duration_display(self, obj):
        return str(obj.duration).split(".")[0] if obj.duration else "-"


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
    unfold.admin.ModelAdmin,
):
    compressed_fields = True
    list_fullwidth = True
    list_filter_sheet = False

    list_display = [
        # "user_identity",
        "time_online",
        "user_display",
        "time_since_last_heartbeat_in_seconds",
        # "created",
        "player_source_display",
        "player_state_display",
        "user_agent_display",
        "remote_ip",
        "foreground_display",
        "online_display",
    ]
    list_filter = [
        ("time", IsOnlineFilter),
        DeviceFilter,
        "in_foreground",
        "player_source",
        "player_state",
    ]
    search_fields = [
        "user_identity",
        "user_agent",
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
    inlines = [
        PlayerEventInline,
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by("-created")
        return qs

    ###################################################################
    # display
    ###################################################################
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

    @unfold.decorators.display(
        description="source",
        label=True,
    )
    def player_source_display(self, obj):
        return obj.player_source

    @unfold.decorators.display(
        description="state",
        label={
            "playing": "success",
        },
    )
    def player_state_display(self, obj):
        return obj.player_state

    @unfold.decorators.display(
        description="mode",
        label={
            "foreground": "success",
        },
    )
    def foreground_display(self, obj):
        return "foreground" if obj.in_foreground else "background"

    @unfold.decorators.display(
        description="online",
        label={
            "online": "success",
        },
    )
    def online_display(self, obj):
        if obj.time_since_last_heartbeat.total_seconds() < IS_ONLINE_THRESHOLD:
            return "online"

        return "offline"
