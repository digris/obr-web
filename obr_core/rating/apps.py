from django.apps import AppConfig


class RatingConfig(AppConfig):
    name = "rating"
    verbose_name = "Rating App"

    def ready(self):
        import rating.signals  # noqa
