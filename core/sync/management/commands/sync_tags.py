from django.core.management.base import BaseCommand, CommandError
from django.db.models.functions import Now

from tagging.models import Tag
from tagging.sync.tag import sync_tag


class Command(BaseCommand):
    help = "Sync tag(s) from OBP"

    def add_arguments(self, parser):
        parser.add_argument(
            "tag_uids",
            nargs="*",
            type=str,
        )
        parser.add_argument(
            "--delete",
            dest="delete",
            action="store_true",
            help="delete tags that are not (anymore) on OBP",
        )
        parser.add_argument(
            "--database",
            type=str,
            default="default",
        )

    def handle(self, *args, **options):

        qs = Tag.objects.using(options["database"]).all()

        if tag_uids := options["tag_uids"]:
            qs = qs.filter(uid__in=tag_uids)
            if qs.count() < 1:
                raise CommandError(f"no tags for uid: {', '.join(tag_uids)}")

        self.stdout.write(f"num. tags to sync: {qs.count()}")

        for tag in qs:
            sync_tag(tag, delete=options["delete"])

        qs.update(
            sync_last_update=Now(),
        )
