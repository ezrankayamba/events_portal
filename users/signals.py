from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def notify_created(user):
    sub = 'Successful regitstraion'
    html_content = render_to_string(
        'users/created_user_mail.html', {'user': user})
    msg = f'You have been successfully created as username: {user.username}. Default password is Fiesta19. Events Portal is accessible at https://www.pincomtz.net'
    sender = 'Events Portal<nezatech.notifications@gmail.com>'
    to = [user.email]
    send_mail(sub, msg, sender, to, fail_silently=False,
              html_message=html_content)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        notify_created(instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
