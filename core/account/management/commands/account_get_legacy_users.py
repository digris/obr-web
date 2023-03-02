from django.core.management.base import BaseCommand

from account import migrator


class Command(BaseCommand):
    help = "Update legacy user accounts (information used during user creation)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            dest="database",
            type=str,
            default="default",
        )

    def handle(self, *args, **options):
        migrator.obp.update_legacy_users(
            database=options["database"],
        )
