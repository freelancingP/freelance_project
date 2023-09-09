# Generated by Django 4.2.3 on 2023-09-09 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_engine', '0040_calorycount_dish_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calorycount',
            old_name='dish_type',
            new_name='meal_type',
        ),
        migrations.RemoveField(
            model_name='calorycount',
            name='calory',
        ),
        migrations.RemoveField(
            model_name='calorycount',
            name='dish',
        ),
        migrations.AddField(
            model_name='calorycount',
            name='dishes',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='calorycount',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]