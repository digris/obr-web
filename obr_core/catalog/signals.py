import logging

from django import dispatch

logger = logging.getLogger(__name__)

sync_media_completed = dispatch.Signal()
