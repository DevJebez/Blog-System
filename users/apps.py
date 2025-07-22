from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    def ready(self):
        import users.signals # This ensures that the signals are imported when the app is ready
        # This is necessary to ensure that the signal handlers are connected when the app is loaded.