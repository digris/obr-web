from django.core.management.base import BaseCommand

from account import migrate


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
        # parser.add_argument(
        #     "--email",
        #     dest="email",
        #     type=str,
        #     required=False,
        # )

    def handle(self, *args, **options):
        print(options)

        if options["source"].lower() == "obr":
            print("OBR")
            migrate.migrate_accounts_from_obr(
                database=options["database"],
            )

        if options["source"].lower() == "obp":
            raise NotImplementedError("OBR source not implemented yet")

        # num_migrated = archive.archive_airplays(database=options["database"],)
        # self.stdout.write(f"migrated {num_migrated} accounts")
