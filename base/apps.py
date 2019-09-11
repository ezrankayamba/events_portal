from django.apps import AppConfig
import threading


class BaseConfig(AppConfig):
    name = 'base'
    verbose_name = "Base Module"

    def ready(self):
        from nots import background
        print(f'The base application is now running')
        # threading.Thread(target=background.mail_reader_thread).start()
