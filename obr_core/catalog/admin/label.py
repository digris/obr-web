from django.contrib import admin
from django.db.models import Count

import unfold.admin
import unfold.contrib.filters.admin
import unfold.decorators
from catalog.models.label import Label, LabelImage
from identifier.admin import IdentifierInline
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image
from sync.admin import SyncAdminMixin, sync_qs_action


class LabelImageInline(SortableImageInlineMixin):
    model = LabelImage


@admin.register(Label)
class LabelAdmin(SyncAdminMixin, unfold.admin.ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth = True
    list_filter_sheet = False

    date_hierarchy = "created"
    list_display = [
        "image_display",
        "label_display",
        "kind_display",
        "num_releases_display",
        "num_children_display",
        "sync_last_update",
        "sync_state_display",
        "uid_display",
    ]
    list_filter = [
        "kind",
        "sync_state",
    ]
    search_fields = [
        "name",
        "uid",
    ]
    readonly_fields = [
        "uuid",
        "uid",
        "tags",
        #
        "updated",
    ]
    autocomplete_fields = [
        "root",
    ]
    inlines = [
        LabelImageInline,
        IdentifierInline,
    ]
    actions = [
        sync_qs_action,
    ]

    def get_queryset(self, request):  # pragma: no cover
        qs = super().get_queryset(request)
        qs = qs.prefetch_related(
            "images",
        )
        qs = qs.annotate(
            num_releases=Count(
                "releases",
                distinct=True,
            ),
        )
        return qs

    ###################################################################
    # display
    ###################################################################
    @admin.display(
        description="Image",
    )
    def image_display(self, obj):  # pragma: no cover
        return get_admin_inline_image(obj.image)

    @unfold.decorators.display(
        description="label",
        header=True,
        ordering="name",
    )
    def label_display(self, obj):
        return obj.name, obj.root or "-"

    @unfold.decorators.display(
        description="type",
        header=True,
        ordering="kind",
    )
    def kind_display(self, obj):
        return obj.get_kind_display(), obj.root.get_kind_display() if obj.root else "-"

    @admin.display(
        description="releases",
        ordering="num_releases",
    )
    def num_releases_display(self, obj):  # pragma: no cover
        return obj.num_releases or "-"

    @admin.display(
        description="sub-labels",
    )
    def num_children_display(self, obj):  # pragma: no cover
        return obj.children.count() or "-"

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid
