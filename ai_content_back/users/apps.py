from django.apps import AppConfig


class UsersConfig(AppConfig):
    """signals added to users app"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals  # Add this line to import the signals.py
