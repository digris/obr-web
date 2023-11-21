from django.urls import resolve, reverse


class TestArtistUrls:
    def test_artist_list_url(self):
        path = reverse("api:catalog:artist-list")
        assert resolve(path).view_name == "api:catalog:artist-list"

    def test_artist_detail_url(self):
        path = reverse("api:catalog:artist-detail", kwargs={"uid": "F0000000"})
        assert resolve(path).view_name == "api:catalog:artist-detail"
