from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class Tagdmin(admin.ModelAdmin):
    save_on_top = True

    list_display = [
        "name",
        "uid",
        "type",
        "num_tagged_items",
    ]
    list_filter = [
        "type",
    ]
    search_fields = [
        "name",
        "uid",
    ]
    readonly_fields = [
        "uid",
        "uuid",
    ]

    @admin.display(
        description="Num. items",
    )
    def num_tagged_items(self, obj):
        return f"{obj.tagging_taggeditem_items.count()}"
