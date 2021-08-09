# -*- coding: utf-8 -*-
from django.utils import timezone

from broadcast.models import Emission


def get_current_item():
    current_emission = Emission.objects.current().first()
    if not current_emission:
        return None
    now = timezone.now()
    media_set = current_emission.get_media_set()
    return next((m for m in media_set if m["time_start"] < now <= m["time_end"]), None)


def get_current_media():
    current_item = get_current_item()
    if not current_item:
        return None
    return current_item.get("media", None)
