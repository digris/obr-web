import logging
import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from account.models import User, MigrationSource

OBR_SYNC_ENDPOINT = getattr(settings, "OBR_SYNC_ENDPOINT", None)
OBR_SYNC_TOKEN = getattr(settings, "OBR_SYNC_TOKEN", None)

logger = logging.getLogger(__name__)


class OBRMigrator:
    def __init__(self, database="default"):
        self.endpoint = OBR_SYNC_ENDPOINT
        self.token = OBR_SYNC_TOKEN
        self.database = database

        try:
            assert self.endpoint
            assert self.token
        except AssertionError as e:
            raise ImproperlyConfigured(
                "missing OBR_SYNC_ENDPOINT and / or OBR_SYNC_TOKEN"
            ) from e

        self.headers = {
            "Authorization": f"Token {self.token}",
        }

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

        logger.info(f"loaded {len(user_accounts)} accounts from remote API")

        for user_account in user_accounts:
            email = user_account.get("email")
            obp_id = user_account.get("obp_id")
            first_name = user_account.get("first_name")
            last_name = user_account.get("last_name")
            date_joined = user_account.get("date_joined")
            last_login = user_account.get("last_login")

            if not email:
                logger.warning(f"unable to get email for {user_account}")

            try:
                user = User.objects.get(email=user_account["email"])
                logger.info(f"existing account: {email}")
                User.objects.filter(id=user.id,).update(
                    date_joined=date_joined,
                )
            except User.DoesNotExist as e:
                user = User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    date_joined=date_joined,
                    last_login=last_login,
                    obp_id=obp_id,
                    migration_source=MigrationSource.OBR,
                )
                user.set_unusable_password()
                user.save()
                # logger.info(f'missing account: {email}')

            # print(user_account)


def migrate_accounts_from_obr(database="default"):
    migrator = OBRMigrator(database=database)
    return migrator.migrate()
