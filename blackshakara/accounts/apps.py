from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blackshakara.accounts'

    def ready(self):
        import blackshakara.accounts.signals  # noqa: F401
