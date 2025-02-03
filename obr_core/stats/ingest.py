import base64
import hashlib
import json
import logging
from datetime import datetime, timedelta

from django.db import connections

import elasticsearch
import elasticsearch.helpers
from account.models import User
from rating.models import Vote

LOGGER = logging.getLogger(__name__)


EVENT_MIN_DURATION = 20


ES_HOST = "49.13.151.17"
ES_PORT = 9200
ES_API_KEY = "d0p4UHE1TUJ5azF4Y21YazZYVGE6UFl5aTZOajZTSFc1N0tHcGdyYURDZw=="

GEOIP_DICT = {
    "country": None,
    "region": None,
    "city": None,
}

USER_DICT = {
    "uid": "",
    "email": "",
}

SESSION_DICT = {
    "_id": None,
    "origin": None,
    #
    "time_start": None,
    "time_end": None,
    #
    "duration_s": 0,
    "duration_playing_s": 0,
    "duration_playing_live_s": 0,
    "duration_playing_ondemand_s": 0,
    #
    "bytes_sent": 0,
    #
    "remote_addr": None,
    #
    "path": None,
    "referer": "",
    "user_agent": None,
    #
    "device_key": None,
    "user_identity": None,
    "user": None,
    #
    "geoip": None,
    #
    "aggregator": None,
}


class IngestError(Exception):
    pass


def encode_sha1(value):
    hashed_value = hashlib.sha1()  # NOQA: S324
    hashed_value.update(value.encode("ascii"))
    return hashed_value.hexdigest()


def encode_base64(value):
    return base64.b64encode(value.encode("ascii")).decode("ascii")


def parse_ua_aggregator(ua: str) -> str | None:  # noqa C901
    ua = ua.lower() if ua else ""

    if "tunein" in ua:
        return "tunein"

    if "onestream iptv" in ua:
        return "onestream"

    if "icecast" in ua:
        return "icecast"

    if "dabplayer" in ua:
        return "dabplayer"

    if "onlineradiobox hisbot" in ua:
        return "histbot"

    if "sonos/" in ua:
        return "sonos"

    if "mytuner" in ua:
        return "mytuner"

    if "radioplayer" in ua:
        return "radioplayer"

    return None


def generate_device_key(ip: str, ua: str) -> str:
    if not (ip and ua):
        return ""

    parts = [
        encode_base64(ip),
        encode_sha1(ua)[:10],
    ]

    return "-".join(parts)


class EsService:
    client: elasticsearch.Elasticsearch

    def __init__(self):
        self.client = elasticsearch.Elasticsearch(
            f"https://{ES_HOST}:{ES_PORT}",
            api_key=ES_API_KEY,
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=2,
        )

    def ingest(self, index: str, entries: list[dict]):
        try:
            elasticsearch.helpers.bulk(
                self.client,
                entries,
                index=index,
                pipeline="ua-geoip",
            )
        except elasticsearch.TransportError as e:
            LOGGER.warning(f"failed to index documents: {e}")
            raise IngestError(f"failed to index documents: {e}") from e
        except elasticsearch.helpers.BulkIndexError as e:
            LOGGER.warning(f"failed to index documents: {e}")
            print(e.__dict__)
            raise IngestError(f"failed to index documents: {e}") from e


def get_player_sessions(
    database="default",
    time_from: datetime | None = None,
    time_until: datetime | None = None,
):
    time_starts_str = (
        time_from.strftime("%Y-%m-%d %H:%M:%S") if time_from else "2000-01-01 00:00:00"
    )
    time_until_str = (
        time_until.strftime("%Y-%m-%d %H:%M:%S")
        if time_until
        else "3000-12-31 00:00:00"
    )

    query = f"""
    WITH ordered_events AS (
        SELECT *,
               LAG(time_end)
               OVER (PARTITION BY user_identity, device_key ORDER BY time) as prev_time_end
        FROM stats_player_event
        WHERE
            time >= '{time_starts_str}'
            AND time <= '{time_until_str}'
            AND state = 'playing'
    ),
    events AS (
        SELECT *,
               SUM(CASE WHEN EXTRACT(EPOCH FROM (time - prev_time_end)) > 30 THEN 1 ELSE 0 END)
               OVER (PARTITION BY user_identity, device_key ORDER BY time) as group_id
        FROM ordered_events
    )
    SELECT MIN(time) as time_start,
           MAX(time_end) as time_end,
           EXTRACT(EPOCH FROM (MAX(time_end) - MIN(time))) as duration_s,
           SUM(calculated_duration_s) as duration_playing_s,
           SUM(CASE WHEN source = 'live' THEN calculated_duration_s ELSE 0 END) as duration_playing_live_s,
           SUM(CASE WHEN source = 'on-demand' THEN calculated_duration_s ELSE 0 END) as duration_playing_ondemand_s,
           user_identity,
           device_key,
           convert_from(decode(split_part(device_key, '-', 1), 'base64'), 'UTF8') as remote_addr
    FROM events
    GROUP BY user_identity, device_key, group_id
    HAVING SUM(calculated_duration_s) >= {EVENT_MIN_DURATION}
    ORDER BY time_start;
    """

    print(query)

    with connections[database].cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]  # noqa B905

    return results


def get_stream_sessions(
    database="default",
    time_from: datetime | None = None,
    time_until: datetime | None = None,
):
    time_starts_str = (
        time_from.strftime("%Y-%m-%d %H:%M:%S") if time_from else "2000-01-01 00:00:00"
    )
    time_until_str = (
        time_until.strftime("%Y-%m-%d %H:%M:%S")
        if time_until
        else "3000-12-31 00:00:00"
    )

    query = f"""
    SELECT *,
             EXTRACT(EPOCH FROM (time_end - time_start)) as duration_s
             FROM stats_stream_event
             WHERE seconds_connected >= {EVENT_MIN_DURATION}
             AND time_start >= '{time_starts_str}'
             AND time_end <= '{time_until_str}'
    ORDER BY time_start;
    """

    print(query)

    with connections[database].cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]  # noqa B905

    return results


def ingest_legacy_stream_sessions(
    database="default",
    index_prefix="",
):
    path = "data/stats/stream-events.json"
    with open(path) as f:
        data = json.load(f)

    raw = data["results"]

    filtered = [f for f in raw if f["seconds_connected"] >= EVENT_MIN_DURATION]

    print(f"raw:       {len(filtered)} sessions")

    sessions = []
    for r in filtered:
        s = SESSION_DICT.copy()
        s.update(
            {
                "_id": hashlib.md5(  # noqa S324
                    f"{r['time_start']}{r['time_end']}".encode(),
                ).hexdigest(),
                "origin": "icecast",
                "time_start": r["time_start"],
                "time_end": r["time_end"],
                "duration_s": r["seconds_connected"],
                "duration_playing_s": r["seconds_connected"],
                "duration_playing_live_s": r["seconds_connected"],
                "bytes_sent": r["bytes_sent"],
                "remote_addr": r["ip"],
                "path": r["path"],
                "referer": r.get("referer", ""),
                "user_agent": r["user_agent"],
                "user_agent_short": r.get("user_agent", "")[:25]
                if r["user_agent"]
                else "",
                #
                "aggregator": parse_ua_aggregator(r["user_agent"]),
                "device_key": generate_device_key(r["ip"], r["user_agent"]),
            },
        )

        # NOTE: we run this in pipeline
        # if ip := r['ip']:
        #
        #         pass

        sessions.append(s)

    print(f"annotated: {len(sessions)} sessions")

    es = EsService()
    es.ingest(index_prefix + "listener-sessions", sessions)

    return len(sessions)


def ingest_stream_sessions(
    database="default",
    index_prefix="",
    time_from: datetime | None = None,
    time_until: datetime | None = None,
):
    raw = get_stream_sessions(
        database=database,
        time_from=time_from,
        time_until=time_until,
    )

    print(f"raw:       {len(raw)} sessions")

    sessions = []
    for r in raw:
        s = SESSION_DICT.copy()

        time_start = r["time_start"]
        time_end = r["time_end"]

        if r["origin"] == "hls":
            time_start = time_start + timedelta(hours=1)
            time_end = time_end + timedelta(hours=1)

        # if r["origin"] == "hls":
        #     if r["ip"] == "83.150.2.154":

        if r["ip"] == "83.150.2.154":
            print(time_start, time_end, r["origin"])

        s.update(
            {
                "_id": str(r["uuid"]),
                "origin": r["origin"],
                "time_start": time_start,
                "time_end": time_end,
                "duration_s": r["duration_s"],
                "duration_playing_s": r["duration_s"],
                "duration_playing_live_s": r["duration_s"],
                "bytes_sent": r["bytes_sent"],
                "remote_addr": r["ip"],
                "path": r["path"],
                "referer": r["referer"],
                "user_agent": r["user_agent"],
                "user_agent_short": r.get("user_agent", "")[:25],
                "device_key": r["device_key"],
                #
                "aggregator": parse_ua_aggregator(r["user_agent"]),
            },
        )

        # NOTE: we run this in pipeline
        # if r['geoip_country']:

        sessions.append(s)

    # if sessions:

    print(f"annotated: {len(sessions)} sessions")

    es = EsService()
    es.ingest(index_prefix + "listener-sessions", sessions)
    #
    print(f"inserted:  {len(sessions)} sessions")

    return len(sessions)


def ingest_player_sessions(
    database="default",
    index_prefix="",
    time_from: datetime | None = None,
    time_until: datetime | None = None,
):
    raw = get_player_sessions(
        database=database,
        time_from=time_from,
        time_until=time_until,
    )

    print(f"raw:       {len(raw)} sessions")

    user_cache = {}

    sessions = []
    for r in raw:
        s = SESSION_DICT.copy()
        s.update(
            {
                "_id": hashlib.md5(  # noqa S324
                    f"{r['time_start']}{r['time_end']}".encode(),
                ).hexdigest(),
                "origin": "obr",
                "time_start": r["time_start"],
                "time_end": r["time_end"],
                "duration_s": r["duration_s"],
                "duration_playing_s": r["duration_playing_s"],
                "duration_playing_live_s": r["duration_playing_live_s"],
                "duration_playing_ondemand_s": r["duration_playing_ondemand_s"],
                "remote_addr": r["remote_addr"],
                "path": "play.hls",
                "user_agent": "obr",
                "user_identity": r["user_identity"],
                "device_key": r["device_key"],
                #
                "aggregator": "obr",
            },
        )

        if r["user_identity"].startswith("account.user:"):
            uid = r["user_identity"].replace("account.user:", "")
            u = USER_DICT.copy()

            if user := user_cache.get(uid):
                u["uid"] = user.uid
                u["email"] = user.email
            else:
                user = User.objects.filter(uid=uid).first()
                user_cache[uid] = user
                if user:
                    u["uid"] = user.uid
                    u["email"] = user.email

            s["user"] = u

        sessions.append(s)

    print(f"annotated: {len(sessions)} sessions")

    es = EsService()
    es.ingest(index_prefix + "listener-sessions", sessions)

    print(f"inserted:  {len(sessions)} sessions")

    return len(sessions)


def ingest_users(database="default"):
    qs = User.objects.using(database).all()

    print(f"qs:        {qs.count()} users")

    users = []

    for u in qs:
        users.append(
            {
                "_id": u.uid,
                "@timestamp": u.date_joined,
                "last_login": u.last_login,
                "uid": u.uid,
                "is_staff": u.is_staff,
                "email": u.email,
                #
                "migration_source": u.migration_source,
                "gender": u.gender,
                "country": u.country.code if u.country else None,
                "year_of_birth": u.year_of_birth,
                "favorite_venue": u.favorite_venue,
            },
        )

    es = EsService()
    es.ingest("users", users)

    print(f"inserted:  {len(users)} users")

    return len(users)


def ingest_votes(database="default"):
    qs = Vote.objects.using(database).filter(created__year__gte=2024)
    qs = qs.select_related("user")

    print(f"qs:        {qs.count()} votes")

    votes = []

    for v in qs:
        votes.append(
            {
                "_id": v.uid,
                "@timestamp": v.created,
                "value": v.value,
                "source": v.source,
                "scope": v.scope,
                "user": {"uid": v.user.uid, "email": v.user.email} if v.user else None,
            },
        )

    es = EsService()
    es.ingest("votes", votes)

    print(f"inserted:  {len(votes)} votes")

    return len(votes)
