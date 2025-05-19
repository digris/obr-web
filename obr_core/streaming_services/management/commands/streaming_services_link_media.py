from django.core.management.base import BaseCommand

import streaming_services.services
from catalog.models import Media


class Command(BaseCommand):
    help = "Link media identifiers to streaming services"

    def add_arguments(self, parser):
        parser.add_argument(
            "--provider",
            type=str,
            required=True,
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=100,
        )
        parser.add_argument(
            "--offset",
            type=int,
            default=0,
        )

    def handle(self, *args, **options):

        provider = options["provider"]
        limit = options["limit"]
        offset = options["offset"]

        qs = Media.objects.exclude(
            identifiers__scope=provider,
            kind__in=[
                Media.Kind.JINGLE,
            ],
        )

        num_total = min(limit, qs.count())
        num_linked = 0

        for media in qs[offset : offset + limit]:
            identifier = streaming_services.services.media_link_to_spotify(
                media=media,
            )
            if identifier:
                num_linked += 1
                self.stdout.write(f"linked {identifier} to {media}")
            else:
                self.stdout.write(f"no identifier for {media}")

        self.stdout.write(f"linked {num_linked} of {num_total} media identifiers")
