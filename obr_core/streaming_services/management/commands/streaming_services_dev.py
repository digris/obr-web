from django.core.management.base import BaseCommand

from catalog.models import Media
from streaming_services.api_client import SpotifyAPIClient


class Command(BaseCommand):
    help = "RnD - read spotify track data: 'explicit lyrics'"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=500,
        )
        parser.add_argument(
            "--offset",
            type=int,
            default=0,
        )

    def add_spotify_tracks_data(self, spotify_tracks):
        client = SpotifyAPIClient()

        tracks = spotify_tracks.copy()

        ids = ",".join(i["spotify_id"] for i in tracks)

        data = client.get(
            path="/tracks",
            params={
                "ids": ids,
            },
        )

        # annotate tracks with result data
        for track_data in data.get("tracks", []):
            if track := next(
                (i for i in tracks if i["spotify_id"] == track_data["id"]),
                None,
            ):
                track["spotify_data"] = track_data

        return tracks

    def handle(self, *args, **options):

        limit = options["limit"]
        options["offset"]

        qs = Media.objects.exclude(
            kind__in=[
                Media.Kind.JINGLE,
            ],
        ).filter(
            identifiers__scope="spotify",
        )

        batch_size = min(limit, 50)

        num_total = min(limit, qs.count())
        num_loaded = 0

        spotify_track_results = []

        for start in range(0, num_total, batch_size):
            batch = qs[start : start + batch_size]

            spotify_tracks = []

            for m in batch:
                spotify_tracks.append(
                    {
                        "id": m.id,
                        "spotify_id": m.identifiers.get(scope="spotify").value[14:],
                        "spotify_data": {},
                    },
                )

            spotify_track_results.extend(self.add_spotify_tracks_data(spotify_tracks))

            num_loaded += len(batch)

        explicit_track_ids = []

        for track in spotify_track_results:
            track_id = track["id"]
            spotify_data = track["spotify_data"]

            if spotify_data.get("explicit") is True:
                explicit_track_ids.append(track_id)

        explicit_qs = Media.objects.filter(
            id__in=explicit_track_ids,
        )

        print("num. explicit media:", explicit_qs.count())

        self.stdout.write(f"scanned {num_loaded} of {num_total} media")
