import logging

from django import dispatch

logger = logging.getLogger(__name__)

stripe_webhook_received = dispatch.Signal()
