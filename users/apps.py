from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

#registering signal . py file to the users app
    def ready(self):
        import users.signals
