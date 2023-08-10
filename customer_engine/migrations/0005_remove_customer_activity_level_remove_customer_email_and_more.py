# Generated by Django 4.2.3 on 2023-07-29 10:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customer_engine', '0004_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='activity_level',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='father',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='languages',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='password',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='target_weight',
        ),
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]