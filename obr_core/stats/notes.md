## Player Event Cleanup

```python
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import ExpressionWrapper, DurationField, F
from django.db.models.functions import Now, Extract
from django.utils import timezone

from catalog.models import Media
from stats.models import PlayerEvent

DATABASE = "sync"
MAX_EVENT_DURATION = 4 * 60 * 60  # 4 hours

def get_event_qs():
    qs = PlayerEvent.objects.using(DATABASE)
    return qs

def parse_time(time_str: str):
    return timezone.make_aware(datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S"))


def get_day_ranges(date_start: str, date_end: str, day_start_at_hour: int = 4,):
    
    date_start = datetime.strptime(date_start, "%Y-%m-%d")
    date_end = datetime.strptime(date_end, "%Y-%m-%d")
    
    days = []
    loop_date = date_start
    
    while loop_date <= date_end:
        time_start = timezone.make_aware(datetime.combine(loop_date, datetime.min.time())) + timedelta(hours=day_start_at_hour)
        time_end = time_start + timedelta(hours=24)
        
        days.append({
            "time_start": time_start,
            "time_end": time_end,
        })
        
        loop_date += timedelta(days=1)

    return days


def get_month_ranges(date_start: str, date_end: str, day_start_at_hour: int = 4):
    date_start = datetime.strptime(date_start, "%Y-%m")
    date_end = datetime.strptime(date_end, "%Y-%m")
    
    months = []
    loop_date = date_start
    
    while loop_date <= date_end:
        time_start = timezone.make_aware(datetime.combine(loop_date, datetime.min.time())) + timedelta(hours=day_start_at_hour)
        next_month = loop_date + relativedelta(months=1)
        time_end = timezone.make_aware(datetime.combine(next_month, datetime.min.time())) + timedelta(hours=day_start_at_hour)
        
        months.append({
            "time_start": time_start,
            "time_end": time_end,
        })
        
        loop_date = next_month

    return months



def set_events_time_end_by_next_event(qs):
    qs = qs.annotate_times_and_durations().filter(time_end__isnull=True,).annotate(
        annotated_max_time_end=F("time") + F("max_duration"),
    ).exclude(
        annotated_time_end=None,
    )
    
    # playing_events = [e for e in qs if e.state == PlayerEvent.State.PLAYING]
    
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
    if updated_events:
        PlayerEvent.objects.using(DATABASE).bulk_update(updated_events, ["time_end"])
        
    if num := len(updated_events):
        print("updated by next event:", num)


def set_events_time_end_by_max_duration(qs):
    qs = qs.annotate(
        annotated_max_time_end=F("time") + F("max_duration"),
    ).filter(
        time_end__isnull=True,
        annotated_max_time_end__lt=Now(),
        state=PlayerEvent.State.PLAYING,
    )
    # and set the time_end field
    num_updated = qs.update(
        time_end=F("annotated_max_time_end"),
    )
    if num_updated:
        print("updated by max d:     ", num_updated)


def fix_events_duration(qs):
    qs = qs.annotate_times_and_durations()

    updated_events = []

    for event in [e for e in qs if e.time_end and e.annotated_time_end and e.state == PlayerEvent.State.PLAYING]:
        dur = event.time_end - event.time
        annotated_dur = event.annotated_time_end - event.time

        diff = dur - annotated_dur

        if diff.total_seconds() > 0:
            print(f"{event.id} diff: {diff.total_seconds()}")

            event.time_end = event.annotated_time_end
            updated_events.append(event)

    # update all changed events
    PlayerEvent.objects.using(DATABASE).bulk_update(updated_events, ["time_end"])
        
    if num := len(updated_events):
        print("updated by duration:  ", num)


def fix_events_duration_2(qs):
    qs = qs.annotate_duration().annotate_times_and_durations()
    updated_events = []
    for event in [e for e in qs if e.state == PlayerEvent.State.PLAYING and e.duration is not None and e.annotated_duration is not None]:
        if event.duration <= timedelta(seconds=1) < event.annotated_duration:
            event.time_end = event.time + event.annotated_duration
            updated_events.append(event)
        pass
    
    PlayerEvent.objects.using(DATABASE).bulk_update(updated_events, ["time_end"])
        
    if num := len(updated_events):
        print("updated by duration 2:", num)


days = get_day_ranges("2024-05-01", "2024-06-30")

months = get_month_ranges("2023-01", "2023-12")

# for r in months:
for r in days:
    time_start = r["time_start"]
    time_end = r["time_end"] + timedelta(seconds=MAX_EVENT_DURATION)
    qs = get_event_qs()
    qs = qs.filter(
        time__range=(time_start, time_end),
    )
    # play events without time_end
    qs2 = qs.filter(
        state=PlayerEvent.State.PLAYING,
        time_end__isnull=True,
    )
    # debug output
    print(f"{time_start.date()}: total {qs.count()} events - 'playing' without time_end: {qs2.count()}")
    
    set_events_time_end_by_next_event(qs)
    set_events_time_end_by_max_duration(qs)
    fix_events_duration(qs)
    fix_events_duration_2(qs)
    

for r in days:
    time_start = r["time_start"]
    time_end = r["time_end"] + timedelta(seconds=3600)
    qs = PlayerEvent.objects.using(DATABASE).annotate(
        duration=F("time_end") - F("time"),
    ).filter(
        state=PlayerEvent.State.PLAYING,
        time__range=(time_start, time_end),
        calculated_duration_s__lt=1,
        duration__gte=timedelta(seconds=1),
    )
    print(f"{time_start.date()}: {qs.count()} events with calculated_duration_s < 1")
    if qs.count():
        qs.update(
            calculated_duration_s=ExpressionWrapper(
                Cast(Extract(F('time_end') - F('time'), 'epoch'), output_field=DecimalField(max_digits=10, decimal_places=3)),
                output_field=DecimalField(max_digits=10, decimal_places=3)
            )
        )


# fix where max_duration is 0
# one-time fix - already applied to db
qs = PlayerEvent.objects.using(DATABASE).filter(
    state=PlayerEvent.State.PLAYING,
    max_duration__lt=timedelta(seconds=1)
)
for e in qs:
    _, media_uid = e.obj_key.split(":")
    try:
        media = Media.objects.using(DATABASE).get(uid=media_uid)
        PlayerEvent.objects.using(DATABASE).filter(pk=e.pk).update(max_duration=media.duration)
        print(f"{media_uid}: max duration set to {media.duration}")
    except Media.DoesNotExist:
        print(f"{media_uid}: media not found")

```

## Duration Annotations

```python
from funcy import print_durations
from datetime import timedelta
from django.db.models import ExpressionWrapper, DurationField, IntegerField, F
from django.db.models.functions import Now, Extract
from stats.models import PlayerEvent

DATABASE = "sync"

base_qs = PlayerEvent.objects.using(DATABASE).annotate(
    duration=F("time_end") - F("time"),
)

qs = base_qs.filter(
    state=PlayerEvent.State.PLAYING,
    duration__gt=timedelta(seconds=5),
)


base_qs2 = PlayerEvent.objects.using(DATABASE).annotate(
    duration=ExpressionWrapper(
        F("time_end") - F("time"),
        output_field=DurationField()
    )
)

qs2 = base_qs2.filter(
    state=PlayerEvent.State.PLAYING,
    duration__gt=timedelta(seconds=5),
)


@print_durations
def dbg():
    print(qs.count())

@print_durations
def dbg2():
    print(qs2.count())


for _ in range(10):
    dbg()

for _ in range(10):
    dbg2()

base_qs = PlayerEvent.objects.using(DATABASE)
qs = base_qs.filter(
    state=PlayerEvent.State.PLAYING,
    time__year=2022,
    time_end__isnull=False,
    calculated_duration_s=0,
)

qs.update(
    # calculated_duration_s=ExpressionWrapper(F('time_end') - F('time'), output_field=DurationField())
    calculated_duration_s=ExpressionWrapper(
        Extract(F('time_end') - F('time'), 'epoch'),
        output_field=IntegerField()
    )
)

```

```python
from funcy import print_durations
from datetime import timedelta
from django.db.models import ExpressionWrapper, IntegerField, DecimalField, F
from django.db.models.functions import Extract, Cast
from stats.models import PlayerEvent

DATABASE = "sync"

base_qs = PlayerEvent.objects.using(DATABASE).annotate(
    duration=F("time_end") - F("time"),
)

qs = base_qs.filter(
    state=PlayerEvent.State.PLAYING,
    time__lte="2024-10-29 00:00:00 +01:00",
).exclude(
    time_end__isnull=True,
)

qs.update(
    calculated_duration_s=ExpressionWrapper(
        Cast(Extract(F('time_end') - F('time'), 'epoch'), output_field=DecimalField(max_digits=10, decimal_places=3)),
        output_field=DecimalField(max_digits=10, decimal_places=3)
    )
)


base_qs.filter(
    state=PlayerEvent.State.PLAYING,
    time__lte="2024-10-29 00:00:00 +01:00",
    # duration__gt=timedelta(seconds=5),
    calculated_duration_s__gt=5,
)


@print_durations
def dbg():
    qs_ = base_qs.filter(
        state=PlayerEvent.State.PLAYING,
        time__lte="2024-10-29 00:00:00 +01:00",
        duration__gt=timedelta(seconds=5),
        # calculated_duration_s__gt=5,
    )
    print(qs_.count())

@print_durations
def dbg2():
    qs_ = base_qs.filter(
        state=PlayerEvent.State.PLAYING,
        time__lte="2024-10-29 00:00:00 +01:00",
        # duration__gt=timedelta(seconds=5),
        calculated_duration_s__gt=5,
    )
    print(qs_.count())

    
ids_1 = list(base_qs.filter(
    state=PlayerEvent.State.PLAYING,
    time__lte="2024-10-29 00:00:00 +01:00",
    duration__gt=timedelta(seconds=5),
    # calculated_duration_s__gt=5,
).values_list("id", flat=True))
    
ids_2 = list(base_qs.filter(
    state=PlayerEvent.State.PLAYING,
    time__lte="2024-10-29 00:00:00 +01:00",
    # duration__gt=timedelta(seconds=5),
    calculated_duration_s__gt=5,
).values_list("id", flat=True))


diff = set(ids_1) - set(ids_2)


diff_qs = base_qs.filter(id__in=diff)

```



## Stream Event API

```python
import requests
import time

url = "https://openbroadcast.ch/api/v1/stats/stream-events/?limit=20000"

events = []
next_url = url

time_start = time.time()
while next_url:
    print("loading", next_url)
    r = requests.get(next_url, headers={"Authorization": "Token AQIBWEJUHAPUIDFRHPDXPJNU48"})
    resp = r.json()
    next_url = resp.get("next")
    events.extend(resp.get("results", []))
    
print(f"\nloaded {len(events)} events in {time.time() - time_start:.2f} seconds")
```
    