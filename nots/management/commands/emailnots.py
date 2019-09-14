from django.core.management.base import BaseCommand, CommandError
from nots import background as bg


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Running notifications command!")
        # bg.test_messages()
        bg.mail_reader_thread()
