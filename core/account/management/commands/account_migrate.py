from django.core.management.base import BaseCommand

from account import migrator
from account.models import MigrationSource


class Command(BaseCommand):
    help = "Migrate accounts"

    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            dest="database",
            type=str,
            default="default",
        )
        parser.add_argument(
            "--source",
            dest="source",
            type=str,
            required=True,
            choices=[
                "obr",
                "obp",
            ],
        )
        parser.add_argument(
            "--email",
            dest="email",
            type=str,
            required=False,
        )
        parser.add_argument(
            "--overwrite",
            dest="overwrite",
            action="store_true",
            help="overwrite local account data",
        )

    def handle(self, *args, **options):
        self.stdout.write(str(options))

        emails = [options["email"]] if options["email"] else []

        if options["source"].lower() == MigrationSource.OBR:
            migrator.obr.migrate_accounts(
                database=options["database"],
                emails=emails,
                overwrite=options["overwrite"],
            )

        if options["source"].lower() == MigrationSource.OBP:
            migrator.obp.migrate_accounts(
                database=options["database"],
                emails=emails,
                overwrite=options["overwrite"],
            )
