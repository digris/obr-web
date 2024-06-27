from datetime import timedelta

from django.db.models import F
from django.db.models.functions import Now
from django.utils import timezone

from stats.models import PlayerEvent


def post_process_player_events(database="default"):
    ###################################################################
    # first pass: get unprocessed (no time_end) events where
    # time + max_duration is in the past and older than 24 hours
    ###################################################################
    qs = (
        PlayerEvent.objects.using(database)
        .annotate(
            annotated_max_time_end=F("time") + F("max_duration"),
        )
        .filter(
            time_end__isnull=True,
            annotated_max_time_end__lt=Now(),
            state=PlayerEvent.State.PLAYING,
            time__lt=timezone.now() - timedelta(days=1),
        )
    )

    # and set the time_end field
    # qs.update(

    print("pass 1", qs.count())

    ###################################################################
    # second pass: get unprocessed (no time_end) and update the
    # time_end to the calculated / annotated time
    ###################################################################
    qs = (
        PlayerEvent.objects.using(database)
        .annotate_times_and_durations()
        .filter(
            time__gte=timezone.now() - timedelta(days=1000),
            time_end__isnull=True,
            state__in=[
                PlayerEvent.State.PLAYING,
                # PlayerEvent.State.PAUSED,
                PlayerEvent.State.BUFFERING,
            ],
        )
        .annotate(
            annotated_max_time_end=F("time") + F("max_duration"),
        )
        .exclude(
            annotated_time_end=None,
        )
    )

    # and set the time_end field
    # qs.update does not work here (in combination with window)
    # for event in [e for e in qs if e.annotated_time_end]:
    for event in qs:
        if (
            event.state == PlayerEvent.State.PLAYING
            and event.annotated_time_end
            and event.annotated_max_time_end
        ):
            time_end = min(event.annotated_time_end, event.annotated_max_time_end)
            print("TE", time_end)
        else:
            time_end = event.annotated_time_end

        PlayerEvent.objects.using(database).filter(
            pk=event.pk,
        ).update(
            time_end=time_end,
        )

    count = qs.count()

    print("pass 2", count)

    return count
