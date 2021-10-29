# import pytest
# from django.contrib.admin.sites import AdminSite
# from mixer.backend.django import mixer
# from catalog.models.artist import Artist
# from catalog.admin.artist import ArtistAdmin
# from catalog.models.playlist import Playlist
# from catalog.admin.playlist import PlaylistAdmin
# from catalog.models.release import Release
# from catalog.admin.release import ReleaseAdmin
# from image.utils import get_admin_inline_image
#
#
# @pytest.mark.django_db
# class TestArtistAdmin:
#     def test_image_display(self):
#         artist = mixer.blend(Artist)
#         admin = ArtistAdmin(model=Artist, admin_site=AdminSite())
#         image_display = admin.image_display(obj=artist)
#         assert image_display == get_admin_inline_image(obj=artist)
#
#
# @pytest.mark.django_db
# class TestPlaylistAdmin:
#     def test_image_display(self):
#         playlist = mixer.blend(Playlist)
#         admin = PlaylistAdmin(model=Playlist, admin_site=AdminSite())
#         image_display = admin.image_display(obj=playlist)
#         assert image_display == get_admin_inline_image(obj=playlist)
#
#
# @pytest.mark.django_db
# class TestReleaseAdmin:
#     def test_image_display(self):
#         release = mixer.blend(Release)
#         admin = ReleaseAdmin(model=Release, admin_site=AdminSite())
#         image_display = admin.image_display(obj=release)
#         assert image_display == get_admin_inline_image(obj=release)
#
#     def test_num_media(self):
#         release = mixer.blend(Release)
#         admin = ReleaseAdmin(model=Release, admin_site=AdminSite())
#         num_media = admin.num_media(obj=release)
#         assert num_media == release.media.count()
