import json

from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from mixer.backend.django import mixer
from rating.api.views import ObjectRatingView
from rating.models import Vote
from rest_framework.test import APIRequestFactory

User = get_user_model()


@pytest.mark.django_db
class TestObjectRatingViewAuthenticated:
    # @pytest.fixture(scope="class")
    # def user(self, django_db_setup, django_db_blocker):
    #     with django_db_blocker.unblock():
    #         return mixer.blend(User, email="user@example.org")
    #
    # @pytest.fixture(scope="class")
    # def media(self, django_db_setup, django_db_blocker):
    #     with django_db_blocker.unblock():
    #         return mixer.blend("catalog.Media")

    @pytest.fixture
    def user(self):
        return mixer.blend(User, email="user@example.org")

    @pytest.fixture
    def media(self):
        return mixer.blend("catalog.Media")

    @pytest.fixture
    def path(self, media):
        return reverse(
            "api:rating:object-rating",
            kwargs={
                "obj_ct": media.ct,
                "obj_uid": media.uid,
            },
        )

    def test_get_non_existent_vote(self, user, media, path):
        request = APIRequestFactory().get(path)
        request.user = user
        view = ObjectRatingView.as_view()
        response = view(
            request,
            obj_ct=media.ct,
            obj_uid=media.uid,
        ).render()
        assert response.status_code == 204

    def test_create_vote(self, user, media, path):
        request = APIRequestFactory().post(
            path,
            data={
                "value": 1,
            },
        )
        request.user = user
        view = ObjectRatingView.as_view()
        response = view(
            request,
            obj_ct=media.ct,
            obj_uid=media.uid,
        ).render()
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data.get("value") == 1

    def test_get_vote(self, user, media, path):
        Vote.objects.create(
            user=user,
            content_object=media,
            value=1,
        )
        request = APIRequestFactory().get(path)
        request.user = user
        view = ObjectRatingView.as_view()
        response = view(
            request,
            obj_ct=media.ct,
            obj_uid=media.uid,
        ).render()
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data.get("value") == 1

    def test_delete_vote(self, user, media, path):
        vote = Vote.objects.create(
            user=user,
            content_object=media,
            value=1,
        )
        request = APIRequestFactory().delete(path)
        request.user = user
        view = ObjectRatingView.as_view()
        response = view(
            request,
            obj_ct=media.ct,
            obj_uid=media.uid,
        ).render()
        assert response.status_code == 204
        assert response.content == b""
        assert not Vote.objects.filter(id=vote.id).exists()
