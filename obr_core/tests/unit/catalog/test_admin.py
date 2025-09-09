from django.urls import reverse

import pytest
from catalog.models.release import Release
from mixer.backend.django import mixer


@pytest.mark.django_db
def test_release_change_view_renders(admin_client):
    release = mixer.blend(Release)
    url = reverse("admin:catalog_release_change", args=[release.pk])
    resp = admin_client.get(url)
    assert resp.status_code == 200
    assert b'name="_save"' in resp.content
