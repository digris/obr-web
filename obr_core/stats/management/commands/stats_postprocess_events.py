from django.core.management.base import BaseCommand

from stats import events


class Command(BaseCommand):
    help = "Post-process events (adding end-times, etc.)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            type=str,
            default="default",
        )

    def handle(self, *args, **options):
        num_processed = events.post_process_player_events(database=options["database"])
        self.stdout.write(f"processed {num_processed} events")
