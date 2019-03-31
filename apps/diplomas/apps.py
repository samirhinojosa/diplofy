from django.apps import AppConfig


class DiplomasConfig(AppConfig):
    name = 'apps.diplomas'

    def ready(self):
        import apps.diplomas.signals
