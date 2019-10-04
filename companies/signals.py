from django.db.models.signals import post_save
from .models import Company
from django.dispatch import receiver
from nots import gmail
from . import alias


@receiver(post_save, sender=Company)
def create_profile(sender, instance, created, **kwargs):
    email = get_email()
    if created and email:
        instance.email = email
        instance.save()
        name = instance.name.replace(' ', '')
        service = gmail.init_service()
        gmail.setup_alias(service, name, email)


def get_email():
    a = alias.get_alias('pincomtz.events@gmail.com')
    if a:
        return f'{a}@gmail.com'
    return None
