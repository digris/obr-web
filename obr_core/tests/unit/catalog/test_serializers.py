from datetime import timedelta

import pytest
from catalog.api.serializers.media import DurationInSecondsSerializer
from catalog.api.serializers.playlist import PlaylistSerializer
from catalog.models.media import Media
from catalog.models.playlist import Playlist, Series
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestMediaSerializer:
    def test_duration_in_seconds(self):
        media = mixer.blend(Media, duration=timedelta(seconds=1000))
        serializer = DurationInSecondsSerializer(media.duration)
        assert serializer.to_representation(media.duration) == 1000

    def test_missing_duration_in_seconds(self):
        serializer = DurationInSecondsSerializer(None)
        assert serializer.to_representation(None) == 0


# @pytest.mark.django_db
# class TestPlaylistSerializer:
#     def test_get_series(self):
#         playlist = mixer.blend(Playlist)
#         series = mixer.blend(Series, playlist=playlist)
#         playlist.series = series
#         playlist.series_episode = 1
#         serializer = PlaylistSerializer(playlist)
#         assert serializer.get_series(playlist) == {
#             "ct": "catalog.series",
#             "episode": 1,
#             "uid": series.uid,
#             "name": series.name,
#         }
#
#     def test_missing_get_series(self):
#         playlist = mixer.blend(Playlist)
#         serializer = PlaylistSerializer(playlist)
#         assert serializer.get_series(playlist) is None
