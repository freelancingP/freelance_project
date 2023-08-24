from rest_framework import serializers
from .models import *


class SendOtpSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=15)
    user_type = serializers.CharField(max_length=15)

class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

class BreakfastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Breakfast
        fields = '__all__'

class LaunchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Launch
        fields = '__all__'

class DinnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dinner
        fields = '__all__'

class SnacksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snacks
        fields = '__all__'