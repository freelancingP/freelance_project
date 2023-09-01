from rest_framework import serializers
from .models import *


class SendOtpSerializer(serializers.Serializer):
    email_or_number = serializers.CharField(max_length=50)
    input_type = serializers.CharField(max_length=50)
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

class LunchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lunch
        fields = '__all__'

class DinnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dinner
        fields = '__all__'

class SnacksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snacks
        fields = '__all__'

class DailyRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyRecipe
        fields = '__all__'

class CalorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CaloryCount
        fields = '__all__'