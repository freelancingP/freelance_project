from rest_framework import serializers
from .models import *


class DailySnacksSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailySnacks
        fields = '__all__'

