from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Payment(models.Model):
    payer = models.CharField(max_length=40)
    amount = models.DecimalField(decimal_places=0, max_digits=20)
    record_date = models.DateTimeField(default=timezone.now)
    trans_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.payer

    def get_absolute_url(self):
        return reverse('payment-detail', kwargs={'pk': self.pk})
