from django.core.management.base import BaseCommand

from catalog.models import Media


class Command(BaseCommand):
    help = "RnD - read spotify track data: 'explicit lyrics'"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=500,
        )
        parser.add_argument(
            "--offset",
            type=int,
            default=0,
        )

    def handle(self, *args, **options):

        limit = options["limit"]
        options["offset"]

        qs = Media.objects.exclude(
            kind__in=[
                Media.Kind.JINGLE,
            ],
        ).filter(
            identifiers__scope="spotify",
        )

        batch_size = 50

        num_total = min(limit, qs.count())
        num_loaded = 0

        for start in range(0, num_total, batch_size):
            batch = qs[start : start + batch_size]

            spotify_ids = []
            for m in batch:
                spotify_ids.append(
                    (
                        m.id,
                        m.identifiers.get(scope="spotify").value[14:],
                    ),
                )

            print("spotify_ids", spotify_ids)

            num_loaded += len(batch)

        self.stdout.write(f"linked {num_loaded} of {num_total} media identifiers")
