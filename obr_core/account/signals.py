import logging

from django import dispatch

logger = logging.getLogger(__name__)

user_registered = dispatch.Signal()
