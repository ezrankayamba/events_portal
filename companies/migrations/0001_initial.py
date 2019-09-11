# Generated by Django 2.2.5 on 2019-09-05 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('account', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='companies.Company')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=0, max_digits=20)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='companies.Company')),
                ('company_users', models.ManyToManyField(to='companies.CompanyUser')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]