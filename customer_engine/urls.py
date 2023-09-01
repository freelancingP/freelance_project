from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('send/otp/',views.SendOtpViews.as_view()),
    path('verify/otp/',views.VerifyOtpViews.as_view()),
    path('update/user/details/',views.UpdateUserDetailViews.as_view()),
    path('upload/image/',views.UploadImageView.as_view()),
    path('all/dishes/',views.AllDishesViews.as_view()),
    path('get/dish/',views.GetDishViews.as_view()),
    path('add/calory/',views.AddCaloryViews.as_view()),
    # path('update/daily/recipe/',views.UpdateDailyRecipeViews.as_view()),

]