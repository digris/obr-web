from datetime import timedelta

from django.db.models import DecimalField, ExpressionWrapper, F
from django.db.models.functions import Cast, Extract, Now
from django.utils import timezone

from stats.models import PlayerEvent

MAX_AGE = 4 * 60 * 60  # 4 hours: the longest expected duration of a track


def set_events_time_end_by_next_event(database="default"):
    qs = (
        PlayerEvent.objects.using(database)
        .annotate_times_and_durations()
        .filter(
            time__gte=timezone.now() - timedelta(seconds=MAX_AGE),
            time_end__isnull=True,
            state__in=[
                PlayerEvent.State.PLAYING,
                PlayerEvent.State.BUFFERING,
                PlayerEvent.State.PAUSED,
                PlayerEvent.State.STOPPED,
            ],
        )
        .annotate(
            annotated_max_time_end=F("time") + F("max_duration"),
        )
        .exclude(
            annotated_time_end=None,
        )
    )

    updated_events = []

    for event in qs:
        if (
            event.state == PlayerEvent.State.PLAYING
            and event.annotated_time_end
            and event.annotated_max_time_end
        ):
            time_end = min(event.annotated_time_end, event.annotated_max_time_end)
        elif event.annotated_time_end:
            time_end = event.annotated_time_end

        else:
            continue

        event.time_end = time_end
        updated_events.append(event)

    # update all changed events
    PlayerEvent.objects.using(database).bulk_update(updated_events, ["time_end"])

    return len(updated_events)


def set_events_time_end_by_max_duration(database="default"):
    qs = (
        PlayerEvent.objects.using(database)
        .annotate(
            annotated_max_time_end=F("time") + F("max_duration"),
        )
        .filter(
            time__gte=timezone.now() - timedelta(seconds=MAX_AGE),
            time_end__isnull=True,
            annotated_max_time_end__lt=Now(),
            state=PlayerEvent.State.PLAYING,
        )
    )

    # and set the time_end field
    num_updated = qs.update(
        time_end=F("annotated_max_time_end"),
    )

    return num_updated


def fix_events_duration(database="default"):
    qs = (
        PlayerEvent.objects.using(database)
        .annotate_times_and_durations()
        .filter(
            time__gte=timezone.now() - timedelta(seconds=MAX_AGE),
        )
    )

    updated_events = []

    for event in [e for e in qs if e.time_end and e.annotated_time_end]:
        dur = event.time_end - event.time
        annotated_dur = event.annotated_time_end - event.time

        diff = dur - annotated_dur

        if diff.total_seconds() > 0:
            print(f"{event.id} diff: {diff.total_seconds()}")

            event.time_end = event.annotated_time_end
            updated_events.append(event)

    # update all changed events
    PlayerEvent.objects.using(database).bulk_update(updated_events, ["time_end"])

    return len(updated_events)


def set_events_calculated_duration_s(database="default"):
    qs = PlayerEvent.objects.using(database).filter(
        state=PlayerEvent.State.PLAYING,
        time__gte=timezone.now() - timedelta(seconds=MAX_AGE),
        time_end__isnull=False,
        calculated_duration_s=0,
    )

    num_updated = qs.update(
        calculated_duration_s=ExpressionWrapper(
            Cast(
                Extract(F("time_end") - F("time"), "epoch"),
                output_field=DecimalField(max_digits=10, decimal_places=3),
            ),
            output_field=DecimalField(max_digits=10, decimal_places=3),
        ),
    )

    return num_updated


def post_process_player_events(database="default"):
    num_updated = set_events_time_end_by_next_event(database=database)
    num_updated += set_events_time_end_by_max_duration(database=database)

    num_updated += fix_events_duration(database=database)
    num_updated += set_events_calculated_duration_s(database=database)

    return num_updated
