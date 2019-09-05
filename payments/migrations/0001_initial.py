# Generated by Django 2.2.5 on 2019-09-05 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_id', models.CharField(max_length=40, null=True)),
                ('payer_account', models.CharField(max_length=40)),
                ('payer_name', models.CharField(max_length=40, null=True)),
                ('payee_account', models.CharField(max_length=40, null=True)),
                ('payee_name', models.CharField(max_length=40, null=True)),
                ('amount', models.DecimalField(decimal_places=0, max_digits=20)),
                ('record_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('trans_date', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField()),
                ('unit_price', models.DecimalField(decimal_places=0, max_digits=20)),
                ('ticket_value', models.DecimalField(decimal_places=0, max_digits=20)),
                ('ticket_count', models.IntegerField()),
                ('balance', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('issuer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.CompanyUser')),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='payments.Payment')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.Region')),
            ],
        ),
    ]
