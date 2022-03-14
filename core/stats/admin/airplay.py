from django.contrib import admin
from stats.models import Airplay


@admin.register(Airplay)
class AirplayAdmin(admin.ModelAdmin):
    save_on_top = True
    date_hierarchy = "time_start"
    list_display = [
        "media",
        "time_start",
        "time_end",
    ]
    list_filter = [
        "time_start",
    ]
    search_fields = [
        "uuid",
        "media__uid",
        "media__uuid",
    ]
    readonly_fields = [
        "time_start",
        "time_end",
        "media",
    ]
