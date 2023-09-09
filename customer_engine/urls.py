from rest_framework.routers import DefaultRouter
from  .views import AllDishesViews
from django.urls import path,include

router = DefaultRouter()
router.register(r'all/dishes', AllDishesViews)

urlpatterns = [
    path('', include(router.urls)),
]