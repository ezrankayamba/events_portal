from django.apps import AppConfig
import threading
import os


class BaseConfig(AppConfig):
    name = 'base'
    verbose_name = "Base Module"

    # def ready(self):
    #     from nots import background
    #     print(f'The base application is now running')
    #     run_flag = os.environ.get('RUN_EMAIL_READER', 'ENABLED')
    #     print('Raw run: ', run_flag)

    #     if run_flag == 'ENABLED':
    #         print('Email reader enabled')
    #         # threading.Thread(target=background.mail_reader_thread).start()
    #     else:
    #         print('Email reader disabled!')
