from django.apps import AppConfig


class StreamingServicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "streaming_services"
    verbose_name = "Streaming Services"

    def ready(self):
        import streaming_services.signals  # noqa
