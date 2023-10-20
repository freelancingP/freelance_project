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
    path('recipe/calculator/', views.recipe_calculator, name='recipe_calculator'),
    path('recipe/calculator/<int:id>/', views.recipe_calculator, name='recipe_calculator'),
    path('dish-calculator-items/', views.dish_calculator, name='dish-calculator-items'),
    path('reset/password/', views.reset_password, name='reset_password'),
    path('verify/reset/otp/', views.verify_otp, name='verify_otp'),
    path('set/new/password/', views.new_password, name='new_password'),
    path('customers/detail/<int:user_id>/', views.customers_detail, name='customers_detail'),
    path('customers/detail-more/<int:item_id>/', views.view_more, name='customers_detail_more'),
    path('customers/detail-more/', views.view_more, name='customers_detail_more'),
    path('logout/', views.logout, name='logout'),
    path('add/customer/', views.add_customer, name='add_customer'),
    path('add/dish/', views.add_dish, name='add_dish'),
    path('add/dish/calculator/', views.add_dish_calculator, name='add_dish_calculator'),
    path('add/recipe/', views.add_recipe, name='add_recipe'),
    path('recipe/list/', views.recipe_list, name='recipe_list'),
    path('recipe-detail/', views.recipe_details, name='recipe_details'),
    path('recipe-detail/<int:recipe_id>/', views.recipe_details, name='recipe_details'),
    path('add-ingredient/', views.add_ingredient, name='add_ingredient'),
    # path('add-ingredient', views.add_ingredient, name='add_ingredient'),
    path('ingredient-items/', views.ingredients_items, name='ingredient_items'),
    path('customers/datatable/', views.customers_datatable, name='customers_datatable'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
]
