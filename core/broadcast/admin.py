from django.contrib import admin

from .models import Emission


@admin.register(Emission)
class EmissionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "__str__",
        "uid",
        "time_start",
        "time_end",
        "duration",
        "is_current",
    ]

    list_filter = [
        "time_start",
    ]

    date_hierarchy = "time_start"

    search_fields = [
        "uuid",
    ]

    def is_current(self, obj):
        return obj.is_current

    is_current.boolean = True
