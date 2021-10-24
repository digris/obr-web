import pytest
from catalog.models.artist import Artist, ArtistImage
from catalog.models.mood import Mood
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestArtistModels:
    def test_artist_create(self):
        Artist.objects.create(
            name="Madonna",
        )

    def test_artist_str(self):
        artist = mixer.blend(Artist, name="Madonna")
        assert str(artist) == "Madonna"

    def test_artist_image_str(self):
        artist = mixer.blend(Artist, name="Madonna")
        image = mixer.blend(ArtistImage, artist=artist)
        assert str(image) == str(image.id)


@pytest.mark.django_db
class TestMoodModels:
    def test_create(self):
        Mood.objects.create(
            name="A Mood",
        )

    def test_str(self):
        mood = mixer.blend(Mood, name="A Mood")
        assert str(mood) == "A Mood"

    def test_get_absolute_url(self):
        mood = mixer.blend(Mood)
        assert mood.get_absolute_url() == f"/discover/moods/{mood.uid}/"
