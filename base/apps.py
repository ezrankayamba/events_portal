from django.apps import AppConfig
from nots.views import main as readmail
import time


class BaseConfig(AppConfig):
    name = 'base'
    verbose_name = "Base Application"

    def ready(self):
        print(f'The base application is now running')
        readmail()
