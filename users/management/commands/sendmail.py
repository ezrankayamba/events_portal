from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from nots import gmail
from django.template.loader import render_to_string
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Running sendmail command!")
        sub = 'User created'
        user = User.objects.get(username='fiesta.admin')
        msg = render_to_string('users/created_user_mail.html', {'user': user})

        sender = 'Events Portal<pincomtz.events@gmail.com>'
        to = 'ezrankayamba@gmail.com'
        # send_mail(sub, msg, sender, to, fail_silently=False,)
        service = gmail.init_service()
        message = gmail.create_message(sender, to, sub, msg)
        print(message)
        gmail.send_message(service, message)
