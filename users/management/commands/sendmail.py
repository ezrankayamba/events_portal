from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Running sendmail command!")
        sub = 'User created'
        msg = 'Helloooooooo2'
        sender = 'Events Portal<nezatech.notifications@gmail.com>'
        to = ['ezrankayamba@gmail.com']
        send_mail(sub, msg, sender, to, fail_silently=False,)
