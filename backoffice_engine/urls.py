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
    path('dish-calculator-items', views.dish_calculator, name='dish_calculator_items'),
    path('ingredient-items/', views.ingredients_items, name='ingredient_items'),
    path('reset/password/', views.reset_password, name='reset_password'),
    path('verify/reset/otp/', views.verify_otp, name='verify_otp'),
    path('set/new/password/', views.new_password, name='new_password'),
    path('customers/detail/<int:user_id>/', views.customers_detail, name='customers_detail'),
    path('logout/', views.logout, name='logout'),
    path('add/customer/', views.add_customer, name='add_customer'),
    path('customer', views.customers, name='customer'),
    path('add/dish/', views.add_dish, name='add_dish'),
    path('add/recipe/', views.add_recipe, name='add_recipe'),
    path('recipe/list/', views.recipe_list, name='recipe_list'),
    # path('recipe/details/<int:recipe_id>/', views.recipe_details, name='recipe_details'),
    path('recipe-detail/', views.recipe_details, name='recipe_details'),
    path('recipe-detail/<int:recipe_id>', views.recipe_details, name='recipe_details'),
    path('add_ingredient', views.add_ingredient, name='add_ingredient'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('add/dish/calculator/', views.add_dish_calculator, name='add_dish_calculator'),
    
]