import logging
from django.db import models
from django.db.models.signals import pre_delete
from django.db.utils import IntegrityError
from django.dispatch import receiver

from base.models.mixins import CTUIDModelMixin

from catalog.models import Airplay as CatalogAirplay


logger = logging.getLogger(__name__)


class Airplay(CTUIDModelMixin, models.Model):

    time_start = models.DateTimeField(
        editable=False,
        db_index=True,
        null=False,
        blank=False,
    )

    time_end = models.DateTimeField(
        editable=False,
        db_index=True,
        null=False,
        blank=False,
    )

    media = models.ForeignKey(
        "catalog.Media",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="archived_airplays",
    )

    class Meta:
        app_label = "stats"
        verbose_name = "Airplay (archived)"
        verbose_name_plural = "Airplays (archived)"
        ordering = ["-time_start"]
        get_latest_by = "time_start"

    def __str__(self):
        return f"{self.time_start} - {self.media}"

    @property
    def duration(self):
        return self.time_end - self.time_start


@receiver(pre_delete, sender=CatalogAirplay)
# pylint: disable=unused-argument
def catalog_airplay_pre_delete(sender, instance, **kwargs):
    lookup = {
        "time_start": instance.time_start,
        "time_end": instance.time_end,
        "media": instance.media,
    }
    logger.debug(f"create archived copy for airplay: {instance}")
    try:
        Airplay.objects.get(**lookup)
    except Airplay.DoesNotExist:
        lookup.update(
            {
                "uuid": instance.uuid,
            }
        )
        airplay = Airplay(**lookup)
        try:
            airplay.save()
        except IntegrityError as e:
            logger.warning(f"error archiving airplay {airplay}: {e}")
            pass
