from datetime import datetime

from django.core.management.base import BaseCommand

import stats.ingest


class Command(BaseCommand):
    help = "Ingest events into Elasticsearch"

    source_choices = [
        "stream",
        "player",
        "legacy-stream",
        #
        "user",
        "vote",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            type=str,
            nargs="*",
            choices=self.source_choices,
            help="Source(s) of events to ingest",
        )
        parser.add_argument(
            "--time-from",
            type=datetime.fromisoformat,
            help="Ingest events created AFTER",
        )
        parser.add_argument(
            "--time-until",
            type=datetime.fromisoformat,
            help="Ingest events created BEFORE",
        )
        parser.add_argument(
            "--database",
            type=str,
            default="default",
        )
        parser.add_argument(
            "--index-prefix",
            type=str,
            default="",
        )

    def handle(self, *args, **options):
        source = options["source"] or self.source_choices

        self.stdout.write(f"ingest from: {', '.join(source)}")

        num_ingested = 0

        if "stream" in source:
            try:
                num_ingested += stats.ingest.ingest_stream_sessions(
                    database=options["database"],
                    index_prefix=options["index_prefix"],
                    time_from=options["time_from"],
                    time_until=options["time_until"],
                )
            except stats.ingest.IngestError as e:
                self.stderr.write(f"error ingesting player sessions: {e}")

        if "player" in source:
            try:
                num_ingested += stats.ingest.ingest_player_sessions(
                    database=options["database"],
                    index_prefix=options["index_prefix"],
                    time_from=options["time_from"],
                    time_until=options["time_until"],
                )
            except stats.ingest.IngestError as e:
                self.stderr.write(f"error ingesting player sessions: {e}")

        if "legacy-stream" in source:
            num_ingested += stats.ingest.ingest_legacy_stream_sessions(
                database=options["database"],
                index_prefix=options["index_prefix"],
            )

        if "user" in source:
            num_ingested += stats.ingest.ingest_users(database=options["database"])

        if "vote" in source:
            num_ingested += stats.ingest.ingest_votes(database=options["database"])

        self.stdout.write(f"ingested {num_ingested} docs")
