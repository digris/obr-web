import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse

import pytest
from catalog.api.views import ArtistViewSet, MoodViewSet, PlaylistViewSet
from mixer.backend.django import mixer

User = get_user_model()

# class TestArtistFilter:
#     def test_get_obj_query(self):


@pytest.mark.django_db
class TestArtistViewSet:
    def test_list_anonymous(self):
        mixer.cycle(10).blend("catalog.Artist")
        path = reverse("api:catalog:artist-list")
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        request.user_identity = "aaaa:anonymous-user"
        view = ArtistViewSet.as_view(
            {
                "get": "list",
            }
        )
        response = view(request).render()
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert len(response_data["results"]) == 10

    def test_list_authenticated(self):
        mixer.cycle(10).blend("catalog.Artist")
        path = reverse("api:catalog:artist-list")
        request = RequestFactory().get(path)
        request.user = mixer.blend(User, email="user@example.org")
        view = ArtistViewSet.as_view(
            {
                "get": "list",
            }
        )
        response = view(request).render()
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert len(response_data["results"]) == 10

    def test_retrieve(self):
        artist = mixer.blend("catalog.Artist")
        expected_data = {
            "name": artist.name,
        }
        path = reverse(
            "api:catalog:artist-detail",
            kwargs={
                "uid": artist.uid,
            },
        )
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        view = ArtistViewSet.as_view(
            {
                "get": "retrieve",
            }
        )
        response = view(request, uid=artist.uid).render()
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data.get("name") == expected_data.get("name")


@pytest.mark.django_db
class TestPlaylistViewSet:
    def test_list_anonymous(self):
        mixer.cycle(10).blend("catalog.Playlist")
        path = reverse("api:catalog:playlist-list")
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        request.user_identity = "aaaa:anonymous-user"
        view = PlaylistViewSet.as_view(
            {
                "get": "list",
            }
        )
        response = view(request).render()
        assert response.status_code == 200

    def test_list_authenticated(self):
        mixer.cycle(10).blend("catalog.Playlist")
        path = reverse("api:catalog:playlist-list")
        request = RequestFactory().get(path)
        request.user = mixer.blend(User, email="user@example.org")
        view = PlaylistViewSet.as_view(
            {
                "get": "list",
            }
        )
        response = view(request).render()
        assert response.status_code == 200

    def test_retrieve(self):
        playlist = mixer.blend("catalog.Playlist")
        emission = mixer.blend(
            "broadcast.Emission",
            playlist=playlist,
            time_end="2020-01-01T00:00:00+0200",
        )
        expected_data = {
            "name": playlist.name,
        }
        path = reverse(
            "api:catalog:playlist-detail",
            kwargs={
                "uid": playlist.uid,
            },
        )
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        view = PlaylistViewSet.as_view(
            {
                "get": "retrieve",
            }
        )
        response = view(request, uid=playlist.uid).render()
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data.get("name") == expected_data.get("name")


@pytest.mark.django_db
class TestMoodViewSet:
    def test_list(self):
        mixer.cycle(10).blend("catalog.Mood")
        path = reverse("api:catalog:mood-list")
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        view = MoodViewSet.as_view(
            {
                "get": "list",
            }
        )
        response = view(request).render()
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert len(response_data["results"]) == 10

    def test_retrieve(self):
        mood = mixer.blend("catalog.Mood")
        expected_data = {
            "name": mood.name,
        }
        path = reverse(
            "api:catalog:mood-detail",
            kwargs={
                "uid": mood.uid,
            },
        )
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        view = MoodViewSet.as_view(
            {
                "get": "retrieve",
            }
        )
        response = view(request, uid=mood.uid).render()
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data.get("name") == expected_data.get("name")
