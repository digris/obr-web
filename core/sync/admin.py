# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db.models.functions import Now
from sync.models.mixins import SyncState


@admin.action(description="Re-sync selected")
# pylint: disable=unused-argument
def sync_qs_action(modeladmin, request, queryset):

    for instance in queryset:
        result = instance.sync_data()
        sync_state = SyncState.COMPLETED if result else SyncState.FAILED
        queryset.filter(id=instance.id).update(
            sync_state=sync_state,
            sync_last_update=Now(),
        )
