from django.contrib import admin, messages
from django.shortcuts import redirect

import unfold.admin
import unfold.decorators

from .models import SyncSettings


@admin.register(SyncSettings)
class SyncSettingsAdmin(
    unfold.admin.ModelAdmin,
):
    compressed_fields = True

    date_hierarchy = "updated"
    list_display = [
        "user",
        "provider",
        "remote_uri",
        "social_auth",
    ]
    list_filter = [
        "provider",
    ]
    search_fields = [
        "user__uid",
        "user__email",
        "remote_uri",
    ]
    autocomplete_fields = [
        "user",
    ]
    readonly_fields = [
        "created",
        "updated",
    ]

    actions_row = [
        "sync_from_service",
        "sync_to_service",
    ]
    actions_detail = [
        "sync_from_service",
        "sync_to_service",
    ]

    ###################################################################
    # actions
    ###################################################################
    @unfold.decorators.action(
        description="Sync FROM service",
    )
    def sync_from_service(self, request, object_id):
        obj = self.get_object(request, object_id)

        if True:
            messages.success(request, f"synced {obj.user} FROM: {obj.provider}")
        else:
            messages.error(request, f"failed to sync {obj.user} FROM: {obj.provider}")

        return redirect(request.META["HTTP_REFERER"])

    @unfold.decorators.action(
        description="Sync TO service",
    )
    def sync_to_service(self, request, object_id):
        obj = self.get_object(request, object_id)

        if True:
            messages.success(request, f"synced {obj.user} TO: {obj.provider}")
        else:
            messages.error(request, f"failed to sync {obj.user} TO: {obj.provider}")

        return redirect(request.META["HTTP_REFERER"])
