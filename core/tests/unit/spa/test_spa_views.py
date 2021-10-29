import pytest


@pytest.mark.django_db
def test_spa_index(client):
    url = "/"
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "url",
    [
        "/admin/whatever/missing/",
        "/admin/another/absent/",
    ],
)
def test_spa_302(client, url):
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.parametrize(
    "url",
    [
        "/admin/whatever/missing/",
        "/admin/another/absent/",
    ],
)
def test_spa_404(admin_client, url):
    response = admin_client.get(url)
    assert response.status_code == 404
