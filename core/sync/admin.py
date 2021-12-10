from django.contrib import admin
from django.conf import settings
from django.db.models.functions import Now

from sync.models.mixins import SyncState

SKIP_ALL = getattr(settings, "OBP_SYNC_SKIP_ALL", False)
SKIP_MEDIA = getattr(settings, "OBP_SYNC_SKIP_MEDIA", False)
SKIP_IMAGES = getattr(settings, "OBP_SYNC_SKIP_IMAGES", False)


@admin.action(description="Re-sync selected")
# pylint: disable=unused-argument
def sync_qs_action(modeladmin, request, queryset):

    for instance in queryset:
        if SKIP_ALL:
            continue

        result = instance.sync_data(
            skip_media=SKIP_MEDIA,
            skip_images=SKIP_IMAGES,
        )
        sync_state = SyncState.COMPLETED if result else SyncState.FAILED
        queryset.filter(id=instance.id).update(
            sync_state=sync_state,
            sync_last_update=Now(),
        )
