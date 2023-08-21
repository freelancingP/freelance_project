from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.login,name="login"),
    path('reset/password/',views.reset_password,name="reset_password"),
    path('signup/',views.signup,name="signup"),
    path('dashboard/', views.index, name='dashboard'),
    path('customers/', views.customers, name='customers'),
    path('recipe/management/', views.recipe_management, name='recipe_management'),
    path('dish/calculator/', views.dish_calculator, name='dish_calculator'),
    path('reset/password/', views.reset_password, name='reset_password'),
    path('verify/otp/', views.verify_otp, name='verify_otp'),
    path('set/new/password/', views.new_password, name='new_password'),
    path('customers/detail/<int:user_id>/', views.customers_detail, name='customers_detail'),
    path('logout/', views.logout, name='logout'),
    path('add/customer/', views.add_customer, name='add_customer'),
    path('add/dish/', views.add_dish, name='add_dish'),
    path('add/recipe/', views.add_recipe, name='add_recipe'),
]