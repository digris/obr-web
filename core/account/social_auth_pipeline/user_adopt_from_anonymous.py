from rating.models import Vote
from user_identity.utils import get_anonymous_user_key


# pylint: disable=unused-argument,keyword-arg-before-vararg
def adopt_votes(strategy, user=None, request=None, *args, **kwargs):
    print("strategy", strategy)
    print("user", user)

    user_identity = get_anonymous_user_key(request=request)
    qs = Vote.objects.filter(user_identity=user_identity)

    for vote in qs:
        print("v", vote)

    return
