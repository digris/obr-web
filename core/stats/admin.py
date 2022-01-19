from django.contrib import admin
from .models import PlayerEvent


@admin.register(PlayerEvent)
class PlayerEventAdmin(admin.ModelAdmin):
    list_display = [
        "time",
        "state",
        "obj_key",
        "source",
        "user_identity",
        "device_key",
    ]
    list_filter = [
        "time",
    ]
    search_fields = [
        "obj_key",
        "user_identity",
        "device_key",
    ]
