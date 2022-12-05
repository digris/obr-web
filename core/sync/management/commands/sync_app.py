from django.core.management.base import BaseCommand

from sync.update import update_by_app


class Command(BaseCommand):
    help = "Sync from OBP"

    def add_arguments(self, parser):
        parser.add_argument(
            "app_label",
            type=str,
        )
        parser.add_argument(
            "--max-age",
            type=int,
            default=24 * 60 * 60,
            help="max age / last time updated before n seconds",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=100,
            help="limit number if items to sync per run",
        )

    def handle(self, *args, **options):

        updated = update_by_app(**options)

        for ct in updated:
            print(f"{ct[0]}: \t{ct[1]}")
