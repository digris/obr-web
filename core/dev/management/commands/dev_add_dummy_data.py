from django.core.management.base import BaseCommand, CommandError
from random import randint
from faker import Faker
from datetime import timedelta

from catalog.models import Artist, Media, MediaArtists

fake = Faker()


def fake_artist_name():
    return " ".join(x.capitalize() for x in fake.words(2))


def fake_media_name():
    return " ".join(x.capitalize() for x in fake.words(randint(1, 3)))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=10,
        )

    def handle(self, *args, **options):
        Media.objects.all().delete()
        Artist.objects.all().delete()
        for i in range(0, options["number"]):
            a = Artist(name=fake_artist_name())
            a.save()
        for i in range(0, options["number"]):
            m = Media(
                name=fake_media_name(),
                duration=timedelta(
                    seconds=randint(30, 600),
                ),
            )
            m.save()
            MediaArtists.objects.get_or_create(
                media_id=m.id,
                artist=Artist.objects.order_by("?").first(),
            )
