from django.core.management.base import BaseCommand

from catalog.models import Media
from tagging.utils import get_usage_for_qs


class Command(BaseCommand):
    help = "tagging - dev"

    def handle(self, *args, **options):
        media_qs = Media.objects.filter(name__istartswith="t")
        print("media count", media_qs.count())

        tags = get_usage_for_qs(media_qs, min_count=2)

        for t in tags[:20]:
            print(t.type, t.num_times, t.name)
