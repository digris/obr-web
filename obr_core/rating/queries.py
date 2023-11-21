from django.db.models import Max, NullBooleanField, Q, Value

from .models import Vote, VoteSource


def annotate_qs_width_user_rating(
    qs,
    request,
):
    # annotate with request user's rating
    if request.user.is_authenticated:
        qs = qs.annotate(
            user_rating=Max(
                "votes__value",
                filter=Q(
                    votes__user=request.user,
                ),
            ),
        )
    # annotate with anonymous user 'identity'
    elif hasattr(request, "user_identity"):
        qs = qs.annotate(
            user_rating=Max(
                "votes__value",
                filter=Q(
                    votes__user_identity=request.user_identity,
                ),
            ),
        )
    # make sure we always have `user_rating` annotated
    else:
        qs = qs.annotate(
            user_rating=Value(
                None,
                output_field=NullBooleanField(),
            ),
        )

    return qs


def get_live_ratings_for_time_range(
    time_from,
    time_until,
):
    qs = Vote.objects.filter(
        source=VoteSource.LIVE,
        updated__range=(time_from, time_until),
    )
    return qs
