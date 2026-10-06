from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'

    def ready(self):
        # без этого импорта Django не выполнит signals.py, и сигнал не сработает
        import apps.users.signals  # noqa: F401