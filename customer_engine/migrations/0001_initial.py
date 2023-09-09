# Generated by Django 4.2.3 on 2023-09-09 11:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=1000)),
                ('sub_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('quantity_type', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.FloatField(blank=True, null=True)),
                ('quantity_help', models.CharField(blank=True, max_length=200, null=True)),
                ('type_of_meal', models.CharField(blank=True, max_length=100, null=True)),
                ('type_of_food', models.CharField(blank=True, max_length=100, null=True)),
                ('health_condition', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(blank=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.CharField(blank=True, max_length=100, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('height_unit', models.CharField(blank=True, max_length=10, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('weight_unit', models.CharField(blank=True, max_length=10, null=True)),
                ('health_issue', models.CharField(blank=True, max_length=1000, null=True)),
                ('other_issue', models.CharField(blank=True, max_length=1000, null=True)),
                ('any_medication', models.CharField(blank=True, max_length=500, null=True)),
                ('veg_nonveg', models.CharField(blank=True, max_length=500, null=True)),
                ('profession', models.CharField(blank=True, max_length=200, null=True)),
                ('help', models.CharField(blank=True, max_length=500, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('otp', models.IntegerField()),
                ('status', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DailySnacks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_type', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('Snacks', 'Snacks')], max_length=10)),
                ('food', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.CharField(max_length=10, null=True)),
                ('ingredients', models.CharField(blank=True, max_length=255, null=True)),
                ('veg_nonveg_egg', models.CharField(blank=True, max_length=255, null=True)),
                ('pral', models.FloatField(null=True)),
                ('oil', models.FloatField(null=True)),
                ('gl', models.FloatField(null=True)),
                ('cals', models.FloatField(null=True)),
                ('aaf_adj_prot', models.FloatField(null=True)),
                ('carbs', models.FloatField(null=True)),
                ('total_fat', models.FloatField(null=True)),
                ('tdf', models.FloatField(null=True)),
                ('sodium', models.FloatField(null=True)),
                ('potassium', models.FloatField(null=True)),
                ('phasphorous', models.FloatField(null=True)),
                ('calcium', models.FloatField(null=True)),
                ('magnecium', models.FloatField(null=True)),
                ('total_eaa', models.FloatField(null=True)),
                ('lysine', models.FloatField(null=True)),
                ('gross_protine', models.FloatField(null=True)),
                ('free_suger', models.FloatField(null=True)),
                ('aa_factor', models.FloatField(null=True)),
                ('glucose', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dishes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.CharField(max_length=10, null=True)),
                ('ingredients', models.CharField(blank=True, max_length=255, null=True)),
                ('veg_nonveg_egg', models.CharField(blank=True, max_length=255, null=True)),
                ('pral', models.FloatField(null=True)),
                ('oil', models.FloatField(null=True)),
                ('gl', models.FloatField(null=True)),
                ('cals', models.FloatField(null=True)),
                ('aaf_adj_prot', models.FloatField(null=True)),
                ('carbs', models.FloatField(null=True)),
                ('total_fat', models.FloatField(null=True)),
                ('tdf', models.FloatField(null=True)),
                ('sodium', models.FloatField(null=True)),
                ('potassium', models.FloatField(null=True)),
                ('phasphorous', models.FloatField(null=True)),
                ('calcium', models.FloatField(null=True)),
                ('magnecium', models.FloatField(null=True)),
                ('total_eaa', models.FloatField(null=True)),
                ('lysine', models.FloatField(null=True)),
                ('gross_protine', models.FloatField(null=True)),
                ('free_suger', models.FloatField(null=True)),
                ('aa_factor', models.FloatField(null=True)),
                ('glucose', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_engine.customer')),
                ('dishes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_engine.dailysnacks')),
            ],
        ),
        migrations.CreateModel(
            name='CaloryCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_type', models.CharField(blank=True, max_length=100, null=True)),
                ('dish', models.IntegerField(null=True)),
                ('calory', models.FloatField(default=0.0)),
                ('date', models.DateField(blank=True, null=True)),
                ('total_calory', models.FloatField(default=0.0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_engine.customer')),
            ],
        ),
        migrations.CreateModel(
            name='AddIngridient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingridient_name', models.CharField(max_length=1000)),
                ('quantity_type', models.CharField(blank=True, max_length=100, null=True)),
                ('ingridient_quantity', models.FloatField(null=True)),
                ('protein', models.FloatField(blank=True, null=True)),
                ('calories', models.FloatField(blank=True, null=True)),
                ('fat', models.FloatField(blank=True, null=True)),
                ('carps', models.FloatField(blank=True, null=True)),
                ('sugars', models.FloatField(blank=True, null=True)),
                ('sodium', models.FloatField(blank=True, null=True)),
                ('fiber', models.FloatField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_engine.addrecipe')),
            ],
        ),
    ]
