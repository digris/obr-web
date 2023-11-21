from google.cloud import bigquery  # NOTE: does currently not support python 3.11
from stats.models import PlayerEvent


def player_event_to_row(evt):
    return {
        "time": str(evt.time)[:-6],
        "state": evt.state,
        "duration": evt.duration.seconds if evt.duration else None,
        "obj_key": evt.obj_key,
        "source": evt.source,
        "user_identity": evt.user_identity,
        "device_key": evt.device_key,
    }


def ingest_player_events(database="default"):
    client = bigquery.Client()
    table_id = "open-broadcast.stats.player_event"

    qs = PlayerEvent.objects.using(database).all()

    print(qs.count())

    # Window is disallowed in the filter clause
    # so filtering has to be done in python
    events = [e for e in qs if not e.ingested and e.duration and e.duration.seconds]

    rows = []
    for event in events:
        rows.append(player_event_to_row(event))

    ids = [e.id for e in events]

    if len(rows) > 0:
        client.insert_rows_json(table_id, list(rows))
        qs.filter(id__in=ids).update(ingested=True)

    return len(rows)
