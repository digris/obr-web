import logging

from account.models import MigrationSource, User
from sync import api_client

logger = logging.getLogger(__name__)


class OBPMigrator:
    def __init__(self, database="default"):
        self.database = database
        self.api_client = api_client

    def get_user_accounts(self):
        try:
            params = {
                "limit": 10000,
            }
            data = api_client.get("accounts/", params=params)
            return data.get("results", [])
        except api_client.APIClientException as e:
            logger.error(f"unable to get user: {e}")
            return []

    def migrate(self):
        user_accounts = self.get_user_accounts()
        migrated_accounts = []
        for user_account in user_accounts:
            email = user_account.get("email")
            obp_id = user_account.get("id")
            first_name = user_account.get("first_name")
            last_name = user_account.get("last_name")
            date_joined = user_account.get("date_joined")
            last_login = user_account.get("last_login")

            if not (email and obp_id):
                continue

            try:
                # user = User.objects.get(Q(email=email) | Q(obp_id=obp_id))
                user = User.objects.get(email=email)
                logger.info(
                    f"existing account: {obp_id} - {user.obp_id} / {email} - {user.email}"
                )
            except User.DoesNotExist:
                user = User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    date_joined=date_joined,
                    last_login=last_login,
                    obp_id=obp_id,
                    migration_source=MigrationSource.OBP,
                )
                user.set_unusable_password()
                user.save()
                migrated_accounts.append(email)
                # logger.info(f"new account: {email} - {obp_id}")

        print(f"total: {len(user_accounts)} - created: {len(migrated_accounts)}")


# pylint: disable=unused-argument
def migrate_accounts(
    database="default",
    emails=None,
    overwrite=False,
):
    migrator = OBPMigrator(database=database)
    return migrator.migrate()
