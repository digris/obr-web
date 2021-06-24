# -*- coding: utf-8 -*-
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db.models.functions import Now
from django.utils import timezone
from sync.models.mixins import SyncModelMixin, SyncState


def update_model(model_class, last_update_before):
    qs = model_class.objects.all()
    qs_outdated = model_class.objects.filter(sync_last_update__lt=last_update_before)
    print(
        f"{model_class.__name__}: total: {qs.count()} - outdated: {qs_outdated.count()}"
    )

    for instance in qs_outdated:
        result = instance.sync_data()
        sync_state = SyncState.COMPLETED if result else SyncState.FAILED
        model_class.objects.filter(id=instance.id).update(
            sync_state=sync_state,
            sync_last_update=Now(),
        )


class Command(BaseCommand):
    help = "Sync from OBP"

    def add_arguments(self, parser):
        parser.add_argument(
            "-a",
            "--max-age",
            type=int,
            default=24,
            help="max age / last time updated before n hours",
        )

    def handle(self, *args, **options):
        last_update_before = timezone.now() - timedelta(hours=options["max_age"])
        print("last_update_before", last_update_before)
        for model_class in SyncModelMixin.__subclasses__():
            update_model(model_class=model_class, last_update_before=last_update_before)
