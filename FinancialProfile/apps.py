from django.apps import AppConfig


class FinancialprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FinancialProfile'

    def ready(self):
        import FinancialProfile.signals
