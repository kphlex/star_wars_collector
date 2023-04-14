from django.apps import AppConfig


class RegisterConfig(AppConfig):
    name = 'register'

class UsersConfig(AppConfig):
    name = 'users'
    
    def ready(self):
        import signals