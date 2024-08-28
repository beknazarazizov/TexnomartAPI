from django.apps import AppConfig


class TexnomartUzConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'texnomart_uz'

    def ready(self):
        import texnomart_uz.signals
