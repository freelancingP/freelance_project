from django.contrib import admin
from .models import *
# # Register your models here.

admin.site.register(Customer)
admin.site.register(Dishes)
# admin.site.register(Customer)
# admin.site.register(Lunch)
# admin.site.register(Dinner)
admin.site.register(UserSnacks)
admin.site.register(CaloryCount)
admin.site.register(UserOTP)
admin.site.register(AddRecipe)
admin.site.register(AddIngridient)
admin.site.register(DailySnacks)
admin.site.register(Recipe)
admin.site.register(RecipeIngridient)