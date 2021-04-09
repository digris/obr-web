from django.contrib import admin

from .models import Emission


@admin.register(Emission)
class EmissionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "uuid",
        "__str__",
        "time_start",
    ]

    list_filter = [
        "time_start",
    ]

    date_hierarchy = "time_start"

    search_fields = [
        "uuid",
    ]
