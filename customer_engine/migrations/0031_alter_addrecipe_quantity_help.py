# Generated by Django 4.2.3 on 2023-08-22 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_engine', '0030_addingridient_quantity_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addrecipe',
            name='quantity_help',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
