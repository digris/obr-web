from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserTest(TestCase):
    def setUp(self):
        self.email = "testuser@example.io"
        self.password = "abcd"

        self.test_user = User.objects.create_user(
            email=self.email,
        )

    def test_create_user(self):
        assert isinstance(self.test_user, User)

    def test_default_user_is_active(self):
        assert self.test_user.is_active

    def test_default_user_is_staff(self):
        assert not self.test_user.is_staff

    def test_default_user_is_superuser(self):
        assert not self.test_user.is_superuser

    def test_get_username(self):
        assert self.test_user.get_username() == self.email

    def test_str(self):
        assert self.test_user.__str__() == self.email

    # def test_sync_data(self):
    #     assert self.test_user.sync_data() is None
