from django.core.management.base import BaseCommand
from django.db.models import Q

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
        parser.add_argument(
            "--start-from-uid",
            type=str,
            required=False,
        )

    def handle(self, *args, **options):

        provider = options["provider"]
        limit = options["limit"]
        offset = options["offset"]
        start_from_uid = options["start_from_uid"]

        qs = Media.objects.exclude(
            Q(identifiers__scope=provider)
            | Q(
                kind__in=[
                    Media.Kind.JINGLE,
                ]
            ),
        ).order_by("id")

        if start_from_uid:
            start_from_media = Media.objects.get(uid=start_from_uid)
            qs = qs.filter(id__gte=start_from_media.id)

        num_total = min(limit, qs.count())
        num_linked = 0

        for media in qs[offset : offset + limit]:
            identifier = streaming_services.services.media_link_to_spotify(
                media=media,
            )
            if identifier:
                num_linked += 1
                self.stdout.write(
                    f"linked:     {media.uid} - {media} by: {media.artist_display} to: {identifier.value}"
                )
            else:
                self.stdout.write(
                    f"not linked: {media.uid} - {media} by: {media.artist_display}"
                )

        self.stdout.write(f"linked {num_linked} of {num_total} media identifiers")
