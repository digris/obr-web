
from django.core.management.base import BaseCommand

import stats.annotate


class Command(BaseCommand):
    help = "Annotate events in Elasticsearch"

    kind_choices = [
        "whois",
        "ipintel",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "kind",
            type=str,
            choices=self.kind_choices,
            help="Annotation to perform",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=1000,
            help="Maximum number of unique IPs to annotate (default: 1000)",
        )
        parser.add_argument(
            "--reset-cache",
            action="store_true",
            help="Reset local sqlite cache",
        )

    def handle(self, *args, **options):  # NOQA: C901

        kind = options["kind"]
        limit = options["limit"]
        reset_cache = options["reset_cache"]

        if kind == "whois":
            annotate_func = stats.annotate.annotate_whois
        elif kind == "ipintel":
            annotate_func = stats.annotate.annotate_ipintel
        else:
            self.stderr.write(f"Unknown annotation kind: {kind}")
            return

        cnt, cnt_total = annotate_func(limit=limit, reset_cache=reset_cache)

        self.stdout.write(f"annotated: {kind} - {cnt} unique IPs - {cnt_total} total events")
