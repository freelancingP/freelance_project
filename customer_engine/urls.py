from rest_framework.routers import DefaultRouter
from  .views import AllDishesViewSet
from django.urls import path,include
from . import views
from .views import LoginAPIView, OTPVerifyAPI, DailyCaloryView


router = DefaultRouter()
router.register(r'all/dishes', AllDishesViewSet, basename ="all dishes")


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify-otp/', OTPVerifyAPI.as_view(), name='verify-otp'),

    path('send/otp/',views.SendOtpViews.as_view()),
    path('verify/otp/',views.VerifyOtpViews.as_view()),
    path('update/user/details/',views.UpdateUserDetailViews.as_view()),
    path('upload/image/',views.UploadImageView.as_view()),
    path('daily_calories/', DailyCaloryView.as_view(), name='daily_calories'),





]