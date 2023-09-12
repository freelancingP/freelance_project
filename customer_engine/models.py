from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


class UserProfile(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    otp = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Customer(models.Model):
    image_url = models.URLField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100,blank=True, null=True)
    gender = models.CharField(max_length=100,blank=True, null=True)
    location = models.CharField(max_length=100,blank=True, null=True)
    address = models.CharField(max_length=500,blank=True, null=True)
    contact_number = models.CharField(max_length=15,blank=True, null=True)
    email = models.CharField(max_length=100,blank=True, null=True)
    date_of_birth = models.CharField(max_length=100,blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null=True)
    height_unit = models.CharField(max_length=10,blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null=True)
    weight_unit = models.CharField(max_length=10,blank=True, null=True)
    health_issue = models.CharField(max_length=1000,blank=True, null=True)
    other_issue = models.CharField(max_length=1000,blank=True, null=True)
    any_medication = models.CharField(max_length=500,blank=True, null=True)
    veg_nonveg = models.CharField(max_length=500,blank=True, null=True)
    profession = models.CharField(max_length=200,blank=True, null=True)
    help = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.id)

class UserOTP(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    otp = models.IntegerField()


class CaloryCount(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dish_type = models.CharField(max_length=100,blank=True,null = True)
    dish = models.IntegerField(null = True)
    calory = models.FloatField(default = 0.0)
    date = models.DateField(null=True,blank=True)
    total_calory = models.FloatField(default = 0.0)

    def __str__(self):
        return str(self.calory)
    
    
class DailySnacks(models.Model):
    TYPE_CHOICES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),

    )
    meal_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    food = models.CharField(max_length=200,null=True,blank=True)
    quantity = models.CharField(max_length=10, null=True)
    ingredients = models.CharField(max_length=255,null=True,blank=True)
    veg_nonveg_egg = models.CharField(max_length=255,null=True,blank=True)
    pral = models.FloatField(null=True)
    oil = models.FloatField(null=True)
    gl = models.FloatField(null=True)
    cals = models.FloatField(null=True)
    aaf_adj_prot = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    total_fat = models.FloatField(null=True)
    tdf = models.FloatField(null=True)
    sodium = models.FloatField(null=True)
    potassium = models.FloatField(null=True)
    phasphorous = models.FloatField(null=True)
    calcium = models.FloatField(null=True)
    magnecium = models.FloatField(null=True)
    total_eaa = models.FloatField(null=True)
    lysine = models.FloatField(null=True)
    gross_protine = models.FloatField(null=True)
    free_suger = models.FloatField(null=True)
    aa_factor = models.FloatField(null=True)
    glucose = models.FloatField(null=True)

    def __str__(self):
        return str(self.food)
    

class AddRecipe(models.Model):
    item_name = models.CharField(max_length=1000)
    sub_name = models.CharField(max_length=1000,null=True,blank=True)
    quantity_type = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.FloatField(null=True,blank=True)
    quantity_help = models.CharField(max_length=200,null=True,blank=True)
    type_of_meal = models.CharField(max_length=100,null=True,blank=True)
    type_of_food = models.CharField(max_length=100,null=True,blank=True)
    health_condition = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.item_name


class AddIngridient(models.Model):
    item = models.ForeignKey(AddRecipe, on_delete=models.CASCADE)
    ingridient_name = models.CharField(max_length=1000)
    quantity_type = models.CharField(max_length=100,null=True,blank=True)
    ingridient_quantity = models.FloatField(null=True)
    protein = models.FloatField(null=True,blank=True)
    calories = models.FloatField(null=True,blank=True)
    fat = models.FloatField(null=True,blank=True)
    carps = models.FloatField(null=True,blank=True)
    sugars = models.FloatField(null=True,blank=True)
    sodium = models.FloatField(null=True,blank=True)
    fiber = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.ingridient_name


class DailyRecipe(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dishes = models.ForeignKey(DailySnacks, on_delete=models.CASCADE )

    def __str__(self):
        return self.food

class Dishes(models.Model):
    food = models.CharField(max_length=200,null=True,blank=True)
    quantity = models.CharField(max_length=10, null=True)
    ingredients = models.CharField(max_length=255,null=True,blank=True)
    veg_nonveg_egg = models.CharField(max_length=255,null=True,blank=True)
    pral = models.FloatField(null=True)
    oil = models.FloatField(null=True)
    gl = models.FloatField(null=True)
    cals = models.FloatField(null=True)
    aaf_adj_prot = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    total_fat = models.FloatField(null=True)
    tdf = models.FloatField(null=True)
    sodium = models.FloatField(null=True)
    potassium = models.FloatField(null=True)
    phasphorous = models.FloatField(null=True)
    calcium = models.FloatField(null=True)
    magnecium = models.FloatField(null=True)
    total_eaa = models.FloatField(null=True)
    lysine = models.FloatField(null=True)
    gross_protine = models.FloatField(null=True)
    free_suger = models.FloatField(null=True)
    aa_factor = models.FloatField(null=True)
    glucose = models.FloatField(null=True)

    def __str__(self):
        return self.food



