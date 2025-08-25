from django.conf import settings
from django.contrib import admin, messages
from django.db.models.functions import Now
from django.shortcuts import redirect

import unfold.admin
import unfold.decorators
from sync.models.mixins import SyncState

SKIP_ALL = getattr(settings, "OBP_SYNC_SKIP_ALL", False)
SKIP_MEDIA = getattr(settings, "OBP_SYNC_SKIP_MEDIA", False)
SKIP_IMAGES = getattr(settings, "OBP_SYNC_SKIP_IMAGES", False)


@admin.action(description="Re-sync selected")
# pylint: disable=unused-argument
def sync_qs_action(modeladmin, request, queryset):
    for obj in queryset:
        if SKIP_ALL:
            continue

        if hasattr(obj, "sync_excluded") and obj.sync_excluded:
            continue

        result = obj.sync_data(
            skip_media=SKIP_MEDIA,
            skip_images=SKIP_IMAGES,
        )
        sync_state = SyncState.COMPLETED if result else SyncState.FAILED
        queryset.filter(id=obj.id).update(
            sync_state=sync_state,
            sync_last_update=Now(),
        )


class SyncAdminMixin(unfold.admin.ModelAdmin):

    actions_row = [
        "sync_item",
    ]
    actions_detail = [
        "sync_item",
    ]

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="Sync state",
        ordering="sync_state",
        label={
            "running": "info",
            "completed": "success",
            "failed": "warning",
        },
    )
    def sync_state_display(self, obj):
        return obj.sync_state, obj.sync_last_update

    ###################################################################
    # actions
    ###################################################################
    @unfold.decorators.action(
        description="Sync item",
    )
    def sync_item(self, request, object_id):
        obj = self.get_object(request, object_id)

        if hasattr(obj, "sync_excluded") and obj.sync_excluded:
            messages.info(request, f"sync excluded: {obj}")
            return redirect(request.META["HTTP_REFERER"])

        result = obj.sync_data(
            skip_media=SKIP_MEDIA,
            skip_images=SKIP_IMAGES,
        )

        sync_state = SyncState.COMPLETED if result else SyncState.FAILED

        type(obj).objects.filter(id=obj.id).update(
            sync_state=sync_state,
            sync_last_update=Now(),
        )

        if sync_state == SyncState.COMPLETED:
            messages.success(request, f"synced: {obj}")
        else:
            messages.error(request, f"failed to sync: {obj}")

        return redirect(request.META["HTTP_REFERER"])
