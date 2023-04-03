import logging
from datetime import timedelta

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Now
from django.utils import timezone

from sync.models.mixins import SyncModelMixin, SyncState

logger = logging.getLogger(__name__)

SYNC_APP_LABELS = [
    "account",
    "broadcast",
    "catalog",
]

DEFAULT_LIMIT_PER_RUN = 100


class UpdateError(
    Exception,
):
    pass


def update_for_qs(
    qs,
    last_update_before,
    limit=1000,
):
    """
    run "sync-task" for all instances in queryset that have not been updated (=synced)
    after the given cut-off.
    this takes a while (~seconds) per instance.
    """
    qs_outdated = qs.filter(
        sync_last_update__lt=last_update_before,
    )
    num_outdated = qs_outdated.count()
    num_updated = 0
    logger.info(
        f"{qs.model}: limit: {limit} -  total: {qs.count()} - outdated: {num_outdated}"
    )

    for instance in qs_outdated[0:limit]:
        logger.debug(f"sync: {instance.ct_uid}")
        result = instance.sync_data()
        sync_state = SyncState.COMPLETED if result else SyncState.FAILED
        qs.model.objects.filter(id=instance.id).update(
            sync_state=sync_state,
            sync_last_update=Now(),
        )
        num_updated += 1

    return num_updated


def get_app_models(
    app_label,
):
    """
    get all registered models for given `app_label`
    """
    try:
        return list(apps.get_app_config(app_label).get_models())
    except LookupError:
        return []


def get_sync_content_types(
    models,
):
    """
    get models extending `SyncModelMixin`
    """
    return [
        ContentType.objects.get_for_model(c)
        for c in models
        if c in SyncModelMixin.__subclasses__()
    ]


# pylint: disable=unused-argument
def update_by_app(
    app_label,
    max_age=24 * 60 * 60,
    limit=DEFAULT_LIMIT_PER_RUN,
    **kwargs,
):
    """
    update all "sync-able" (=exchanging data withe remote API) models,
    and run sync flow.
    this is a "maintenance-task" and will be periodically invoked by
    a scheduling tool.
    """

    if app_label not in SYNC_APP_LABELS:
        raise UpdateError(f"not a valid app label: {app_label}")

    app_models = get_app_models(app_label)
    sync_content_types = get_sync_content_types(app_models)

    num_items_per_run = round(limit / len(sync_content_types))
    last_update_before = timezone.now() - timedelta(seconds=max_age)

    updated = []

    for ct in sync_content_types:
        key = f"{ct.app_label}.{ct.model}"
        logger.debug(f"update models: {key}")
        num_updated = update_for_qs(
            qs=ct.model_class().objects.all(),
            last_update_before=last_update_before,
            limit=num_items_per_run,
        )
        updated.append([key, num_updated])

    return updated
