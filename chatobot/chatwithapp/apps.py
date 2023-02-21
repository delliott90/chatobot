from django.apps import AppConfig
from chatwithapp.bot import Bot


class ChatwithappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatwithapp'
