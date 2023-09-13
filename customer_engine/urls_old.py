from django.contrib import admin
from django.urls import path,include
from . import views_old


urlpatterns = [
    path('send/otp/',views_old.SendOtpViews.as_view()),
    path('verify/otp/',views_old.VerifyOtpViews.as_view()),
    path('update/user/details/',views_old.UpdateUserDetailViews.as_view()),
    path('upload/image/',views_old.UploadImageView.as_view()),
    path('all/dishes/',views_old.AllDishesViews.as_view()),
    path('get/dish/',views_old.GetDishViews.as_view()),
    path('add/calory/',views_old.AddCaloryViews.as_view()),
    # path('update/daily/recipe/',views.UpdateDailyRecipeViews.as_view()),

]