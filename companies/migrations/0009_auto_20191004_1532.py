# Generated by Django 2.2.5 on 2019-10-04 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0008_auto_20190911_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='password',
            field=models.CharField(default='notabblicable', max_length=100),
        ),
    ]
