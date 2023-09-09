from .serializers import *
from .models import *
from rest_framework import viewsets

# Create your views here.


class AllDishesViews(viewsets.ModelViewSet):
    queryset = DailySnacks.objects.all()
    serializer_class = DailySnacksSerializer
