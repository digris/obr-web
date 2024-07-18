import pytest
from django.conf import settings

def pytest_collectreport(report):
    if report.failed:
        raise pytest.UsageError("Errors during collection, aborting")


settings.CDN_POLICY_DOMAIN="openbroadcast.ch"