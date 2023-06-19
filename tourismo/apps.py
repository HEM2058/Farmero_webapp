from django.apps import AppConfig


class TourismoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tourismo'

    def ready(self):
          import tourismo.signals  # Import signals module



