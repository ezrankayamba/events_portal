from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from companies.models import Region, CompanyUser


class Payment(models.Model):
    trans_id = models.CharField(max_length=40, null=True)
    payer_account = models.CharField(max_length=40)
    payer_name = models.CharField(max_length=40, null=True)
    payee_account = models.CharField(max_length=40, null=True)
    payee_name = models.CharField(max_length=40, null=True)
    amount = models.DecimalField(decimal_places=0, max_digits=20)
    record_date = models.DateTimeField(default=timezone.now)
    trans_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.trans_id if self.trans_id else 'None'

    def get_absolute_url(self):
        return reverse('payment-detail', kwargs={'pk': self.pk})


class Ticket(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.PROTECT)
    issue_date = models.DateTimeField()
    unit_price = models.DecimalField(decimal_places=0, max_digits=20)
    ticket_value = models.DecimalField(decimal_places=0, max_digits=20)
    ticket_count = models.IntegerField()
    balance = models.DecimalField(decimal_places=0, max_digits=20, null=True)
    issuer = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.payment.trans_id
