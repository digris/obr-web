from __future__ import unicode_literals

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Vote

# from django_elasticsearch_dsl.registries import registry

log = logging.getLogger(__name__)


@receiver(post_save, sender=Vote)
def rating_post_save(sender, instance, created, **kwargs):

    log.debug("rating saved - {} - {}".format(instance.value, instance.content_object))
    # registry.update(instance.content_object)
