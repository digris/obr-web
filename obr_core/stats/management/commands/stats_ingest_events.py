from django.core.management.base import BaseCommand

from stats import ingest


class Command(BaseCommand):
    help = "Ingest events into big-query (NOT IN USE)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            type=str,
            default="default",
        )

    def handle(self, *args, **options):
        num_ingested = ingest.ingest_player_events(database=options["database"])
        self.stdout.write(f"ingested {num_ingested} events")
