# -*- coding: utf-8 -*-
import logging
from django import dispatch

logger = logging.getLogger(__name__)

schedule_updated = dispatch.Signal(
    providing_args=[
        "time_start",
        "time_end",
        "emissions",
    ]
)
