from django.apps import AppConfig


class RatingConfig(AppConfig):
    name = "slack"

    def ready(self):
        import slack.signals  # noqa
