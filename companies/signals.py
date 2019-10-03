from django.db.models.signals import post_save
from .models import Company
from django.dispatch import receiver
from nots import gmail


@receiver(post_save, sender=Company)
def create_profile(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        p1 = email.split('@')
        name = p1[0].split('+')[1]
        service = gmail.init_service()
        gmail.setup_alias(service, name)
