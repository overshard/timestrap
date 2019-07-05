from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"
    verbose_name = "core"

    def ready(self):
        import core.signals  # noqa: F401
