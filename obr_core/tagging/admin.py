from django.contrib import admin
from django.db.models import Count

import unfold.admin
import unfold.decorators

from .models import Tag


@admin.register(Tag)
class Tagdmin(unfold.admin.ModelAdmin):
    save_on_top = True

    list_display = [
        "name",
        "num_tagged_items",
        "type_display",
        "uid_display",
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

    def get_queryset(self, request):  # pragma: no cover
        qs = super().get_queryset(request)
        qs = qs.annotate(
            num_items=Count("tagging_taggeditem_items", distinct=True),
        )
        qs = qs.order_by("-num_items")
        return qs

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="type",
        label=True,
        ordering="type",
    )
    def type_display(self, obj):
        return obj.type

    @admin.display(
        description="Num. items",
        ordering="num_items",
    )
    def num_tagged_items(self, obj):
        return obj.num_items

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid
