from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q

from tagging.models import Tag


def get_usage_for_qs(qs, min_count=None):
    ids = qs.values_list("id", flat=True)

    used_tags_qs = Tag.get_for(qs)

    qs_filter = {
        "id__in": used_tags_qs.values_list(
            "id",
            flat=True,
        ),
    }

    model_cls = type(qs.first())

    if not hasattr(model_cls, "tags"):
        return Tag.objects.none()

    ct = ContentType.objects.get_for_model(qs.model)

    tag_qs = model_cls.tags.get_queryset(
        extra_filters=qs_filter,
    )
    tag_qs = tag_qs.annotate(
        num_times=Count(
            "tagging_taggeditem_items",
            filter=Q(
                tagging_taggeditem_items__content_type=ct,
                tagging_taggeditem_items__object_id__in=ids,
            ),
        ),
    )
    tag_qs = tag_qs.order_by("-num_times")

    if min_count:
        tag_qs = tag_qs.filter(num_times__gte=min_count)

    return tag_qs
