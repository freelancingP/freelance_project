# Generated by Django 4.2.3 on 2023-09-01 02:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customer_engine', '0035_calorycount'),
    ]

    operations = [
        migrations.AddField(
            model_name='calorycount',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
