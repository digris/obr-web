from datetime import timedelta

from django.db.models import F
from django.db.models.functions import Now

from stats.models import PlayerEvent


def post_process_player_events(database="default"):
    ###################################################################
    # first pass: get unprocessed (no time_end) events where
    # time + max_duration is in the past and older than 24 hours
    ###################################################################
    qs = (
        PlayerEvent.objects.using(database)
        .annotate(
            annotated_time_end=F("time") + F("max_duration"),
        )
        .filter(
            time_end__isnull=True,
            annotated_time_end__lt=Now(),
            state=PlayerEvent.State.PLAYING,
            time__lt=Now() - timedelta(days=1),
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
        .annotate(
            annotated_max_time_end=F("time") + F("max_duration"),
        )
        .filter(
            time_end__isnull=True,
            state__in=[
                PlayerEvent.State.PLAYING,
                PlayerEvent.State.PAUSED,
                PlayerEvent.State.BUFFERING,
            ],
        )
        .exclude(
            time__lte=Now() - timedelta(days=10000),
            annotated_time_end=None,
        )
    )

    # and set the time_end field
    # qs.update does not work here (in combination with window)
    print("###")
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

    print("pass 2", qs.count())

    return qs.count()

    #
    #
    # # Window is disallowed in the filter clause
    # # so filtering has to be done in python
    #
