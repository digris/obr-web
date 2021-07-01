from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Q
from django.contrib.contenttypes.models import ContentType

from catalog.models import Media
from tagging.models import Tag


class Command(BaseCommand):
    help = "tagging - dev"

    def handle(self, *args, **options):
        media_qs = Media.objects.filter(name__istartswith="x")
        print("media count", media_qs.count())

        media_ids = media_qs.values_list("id", flat=True)

        # used tags
        tag_qs = Tag.get_for(media_qs)
        print("tag count", tag_qs.count())

        extra_filters = {"id__in": tag_qs.values_list("id", flat=True)}

        # most common
        mc_qs = Media.tags.most_common(min_count=10, extra_filters=extra_filters)
        print("mc count", mc_qs.count())

        # most common
        relname = Media.tags.through.tag_relname()
        relname = "tagging_taggeditem_items"
        mc2_qs = Media.tags.get_queryset(extra_filters=extra_filters)
        # mc2_qs = mc2_qs.annotate(num_times=Count(Media.tags.through.tag_relname()))
        ct = ContentType.objects.get_for_model(media_qs.model)
        mc2_qs = mc2_qs.annotate(
            num_times=Count(
                "tagging_taggeditem_items",
                filter=Q(
                    tagging_taggeditem_items__content_type=ct,
                    tagging_taggeditem_items__object_id__in=media_ids,
                ),
            ),
        )
        mc2_qs = mc2_qs.order_by("-num_times")
        mc2_qs = mc2_qs.filter(num_times__gte=1)
        print("mc2 count", mc2_qs.count())

        print("/////////////////////////////////////////////////////////////////")
        for t in mc2_qs:
            print(t.num_times, t.name)

        for m in media_qs:
            print(m.name)
            print([t.name for t in m.tags.all()])
