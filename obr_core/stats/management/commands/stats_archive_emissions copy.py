from django.core.management.base import BaseCommand

from stats import archive


class Command(BaseCommand):
    help = "Archive emissions to stats db"

    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            type=str,
            default="default",
        )

    def handle(self, *args, **options):
        num_archived = archive.archive_emissions(database=options["database"])
        self.stdout.write(f"archived {num_archived} emissions")
