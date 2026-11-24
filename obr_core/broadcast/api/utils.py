from datetime import timedelta

from django.utils import timezone

import dateutil.parser
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes
from rest_framework.exceptions import ParseError

TIME_RANGE_MAX = timedelta(hours=48)

TIME_RANGE_PARAMETERS = [
    OpenApiParameter(
        name="secondsBack",
        type=OpenApiTypes.INT,
        description="Relative to now. Ignored if `timeFrom` is given.",
    ),
    OpenApiParameter(
        name="secondsAhead",
        type=OpenApiTypes.INT,
        description="Relative to now. Ignored if `timeUntil` is given.",
    ),
    OpenApiParameter(
        name="timeFrom",
        type=OpenApiTypes.DATETIME,
        description="Absolute, e.g. `2023-03-07T08:00:00+01:00`.",
    ),
    OpenApiParameter(
        name="timeUntil",
        type=OpenApiTypes.DATETIME,
        description="Absolute, see `timeFrom`.",
    ),
]


def parse_datetime(value):
    # "+" in an un-encoded query-string arrives as " "
    dt = dateutil.parser.parse(value.replace(" ", "+"))
    return timezone.make_aware(dt) if timezone.is_naive(dt) else dt


def get_time_range(request, now, seconds_back=0, seconds_ahead=0):
    """
    get `(time_from, time_until)` from query-params - either absolute
    (`timeFrom` / `timeUntil`) or relative to now (`secondsBack` / `secondsAhead`).
    """
    try:
        if value := request.GET.get("timeFrom"):
            time_from = parse_datetime(value)
        else:
            seconds_back = int(request.GET.get("secondsBack", seconds_back))
            time_from = now - timedelta(seconds=seconds_back)

        if value := request.GET.get("timeUntil"):
            time_until = parse_datetime(value)
        else:
            seconds_ahead = int(request.GET.get("secondsAhead", seconds_ahead))
            time_until = now + timedelta(seconds=seconds_ahead)
    except (ValueError, OverflowError) as e:
        raise ParseError(f"Invalid filter: {e}") from e

    if time_until - time_from > TIME_RANGE_MAX:
        raise ParseError(f"Range exceeds maximum of {TIME_RANGE_MAX}")

    return time_from, time_until
