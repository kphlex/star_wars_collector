from django.apps import AppConfig
from django.db.models import BigAutoField

class CollectorAppConfig(AppConfig):
    name = 'collector_app'
    default_auto_field = 'django.db.models.BigAutoField'

