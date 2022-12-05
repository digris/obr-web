import re

from django.contrib.auth import get_user_model

import pytest
from freezegun import freeze_time
from subscription.models import Redemption, Voucher
from subscription.models.voucher import generate_code, get_default_code

User = get_user_model()


@pytest.fixture
@freeze_time("2021-01-01 00:00:00", tz_offset=0)
def valid_voucher(db) -> Voucher:
    return Voucher.objects.create()


@pytest.fixture
@freeze_time("2021-01-01 00:00:00", tz_offset=0)
def normal_user(
    db,
) -> User:
    return User.objects.create_user(
        email="normal@user.com",
        password="foo",
    )


@pytest.fixture
@freeze_time("2021-01-01 00:00:00", tz_offset=0)
def redemption(
    db,
    valid_voucher: Voucher,
    normal_user: User,
) -> Redemption:
    voucher = valid_voucher
    user = normal_user
    return Redemption.objects.create(
        voucher=voucher,
        user=user,
    )


@pytest.mark.django_db
# @freeze_time("2021-01-01 00:00:00", tz_offset=0)
def test_voucher_code(
    valid_voucher: Voucher,
) -> None:
    voucher = valid_voucher
    assert len(voucher.code) == 6
    assert len(voucher.code_display) == 8
    assert "".join(voucher.code_display.split("-")) == voucher.code
    assert str(voucher) == voucher.code_display


@pytest.mark.django_db
def test_voucher_num_used(
    valid_voucher: Voucher,
    redemption: Redemption,
) -> None:
    voucher = valid_voucher
    assert voucher.num_used == 1


@pytest.mark.django_db
@freeze_time("2021-01-01 00:00:00", tz_offset=0)
def test_redemtion(
    valid_voucher: Voucher,
    normal_user: User,
) -> None:
    user = normal_user
    voucher = valid_voucher

    redemption = Redemption.objects.create(user=user, voucher=voucher)

    assert str(redemption) == f"{voucher} - {user}"


def test_generate_code() -> None:
    code = generate_code()
    assert len(code) == 6
    assert re.match(r"^[A-Z]{6}$", code) is not None


@pytest.mark.django_db
def test_get_default_code() -> None:
    code = get_default_code()
    assert Voucher.objects.filter(code=code).count() == 0
