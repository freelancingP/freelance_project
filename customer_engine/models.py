from django.db import models
from django.utils import timezone

# Create your models here.


class Customer(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
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
    health_issue = models.CharField(max_length=500,blank=True, null=True)
    other_issue = models.CharField(max_length=500,blank=True, null=True)
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

    
class CustomerStatus(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.status
    
class Dishes(models.Model):
    food = models.CharField(max_length=200,null=True,blank=True)
    quantity = models.CharField(max_length=10, null=True)
    pral = models.FloatField(null=True)
    glycemicload = models.FloatField(null=True)
    oil = models.FloatField(null=True)
    calories = models.FloatField(null=True)
    aaf_adj_prot = models.FloatField(null=True)
    carbohydtrates = models.FloatField(null=True)
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

    def __str__(self):
        return self.food
