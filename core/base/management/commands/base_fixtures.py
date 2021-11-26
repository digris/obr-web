import os
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


FIXTURE_PATH = "./fixtures/"
FIXTURE_SCOPES = [
    {
        "key": "auth",
        "include": [
            "auth",
        ],
        "exclude": [
            "contenttypes",
            "auth.Permission",
            "admin.Logentry",
        ],
        "options": [
            "--natural-foreign",
            "--natural-primary",
        ],
    },
    # {
    #     "key": "accounts",
    #     "include": [
    #         "account",
    #         "social_django",
    #     ],
    #     "exclude": [],
    #     "options": [],
    # },
    {
        "key": "apps",
        "include": [
            "catalog",
        ],
        "exclude": [],
    },
]


class Command(BaseCommand):
    help = "Populate database with sample data"
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
            "task",
            type=str,
            choices=[
                "import",
                "export",
            ],
        )
        parser.add_argument(
            "--database",
            type=str,
            default="default",
            help="database connection to use",
        )

    def handle(self, *args, **options):
        if options["task"] == "import":
            self.import_fixtures(*args, **options)
        elif options["task"] == "export":
            self.export_fixtures(*args, **options)

    def export_fixtures(self, *args, **options):

        verbosity = options["verbosity"]
        database = options["database"]

        for scope in FIXTURE_SCOPES:

            path = os.path.join(FIXTURE_PATH, f"{scope['key']}.yaml")

            excludes = []
            for exclude in scope.get("exclude", []):
                excludes.append("--exclude")
                excludes.append(exclude)

            cmd = [
                "dumpdata",
                *scope.get("include", [scope["key"]]),
                *excludes,
                "--database",
                database,
                *scope.get("options", []),
                "--format",
                "yaml",
                "--indent",
                2,
                "--output",
                path,
            ]

            if verbosity > 1:
                self.stdout.write(" ".join(str(a) for a in cmd))

            call_command(*cmd)

            self.stdout.write(
                self.style.SUCCESS(f'exported [{database}]: {scope["key"]}')
            )

    def import_fixtures(self, *args, **options):

        call_command("migrate")

        database = options["database"]

        if database == "live":
            raise CommandError("import into live database not allowed!")

        for scope in FIXTURE_SCOPES:

            path = os.path.join(FIXTURE_PATH, f"{scope['key']}.yaml")

            call_command(
                "loaddata",
                path,
                "--database",
                database,
            )

            self.stdout.write(
                self.style.SUCCESS(f'imported [{database}]: {scope["key"]}')
            )