import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

OBR_SYNC_ENDPOINT = getattr(settings, "OBR_SYNC_ENDPOINT", None)
OBR_SYNC_TOKEN = getattr(settings, "OBR_SYNC_TOKEN", None)


class OBRMigrator:
    def __init__(self, database="default"):
        self.endpoint = OBR_SYNC_ENDPOINT
        self.token = OBR_SYNC_TOKEN
        self.database = database

        print("endpoint", self.endpoint)
        print("token", self.token)

        try:
            assert self.endpoint
            assert self.token
        except AssertionError as e:
            raise ImproperlyConfigured from e

        self.headers = {"Authorization": f"Token {self.token}"}

    def get_user_accounts(self):
        url = f"{self.endpoint}users/"
        params = {
            "limit": 2000,
        }
        r = requests.get(url=url, params=params, headers=self.headers)
        # print(url)
        # print(r.status_code)
        # print(r.text)
        return r.json()["results"]

    def migrate(self):
        user_accounts = self.get_user_accounts()
        # print(user_accounts)
        print(len(user_accounts))
        # for account in user_accounts:
        #     print(account)


def migrate_accounts_from_obr(database="default"):
    migrator = OBRMigrator(database=database)
    return migrator.migrate()
