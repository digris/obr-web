import pytest


def pytest_collectreport(report):
    if report.failed:
        raise pytest.UsageError("Errors during collection, aborting")
