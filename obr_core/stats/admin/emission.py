from django.contrib import admin

from stats.models import Emission


@admin.register(Emission)
class EmissionAdmin(admin.ModelAdmin):
    save_on_top = True
    date_hierarchy = "time_start"
    list_display = [
        "__str__",
        "obj_key",
        "uid",
        "time_start",
        "time_end",
        "duration",
    ]
    list_filter = [
        "time_start",
    ]
    search_fields = [
        "uuid",
    ]
    readonly_fields = [
        "time_start",
        "time_end",
        "playlist",
    ]
