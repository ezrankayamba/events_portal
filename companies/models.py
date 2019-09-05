from django.db import models
from users.models import Profile
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('companies-home')


class CompanyUser(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.profile.user.username}'


class Region(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=0, max_digits=20)
    company_users = models.ManyToManyField(CompanyUser)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'
