from django.apps import AppConfig


class DonationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "donation"

    def ready(self):
        import donation.signals  # noqa
