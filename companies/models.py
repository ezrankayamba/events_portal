from django.db import models
from users.models import Profile
from django.urls import reverse
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    account = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('companies-home')


class Region(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=0, max_digits=20)

    class Meta:
        ordering = ('name',)
        unique_together = ['name', 'company']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('company-detail', kwargs={'pk': self.company_id})


class CompanyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse('company-detail', kwargs={'pk': self.company_id})
