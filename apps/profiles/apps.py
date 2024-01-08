from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.profiles'

    # make profile app to get notified of the signal
    def ready(self):
        from apps.profiles import signals