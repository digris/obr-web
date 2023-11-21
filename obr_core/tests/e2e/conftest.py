import os

from django.core.management import call_command

import pytest

FIXTURE_PATH = "./obr_core/tests/db-fixtures/"
FIXTURE_FILES = []


@pytest.fixture(scope="module")
def django_db_setup(django_db_setup, django_db_blocker):
    fixture_files = [os.path.join(FIXTURE_PATH, f) for f in FIXTURE_FILES]
    with django_db_blocker.unblock():
        for file in fixture_files:
            call_command("loaddata", file)
