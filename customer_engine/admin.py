from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Dishes)
admin.site.register(UserOTP)
admin.site.register(AddRecipe)
admin.site.register(AddIngridient)