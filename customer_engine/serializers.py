from rest_framework import serializers
from .models import *
# from .models import UserProfile
import random


class UserOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOTP
        fields =  '__all__'

class LoginSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField(default=None, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'otp')
        read_only_fields = ('otp',)


class SendOtpSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=4)
    phone_number = serializers.CharField(max_length=15)
    email = serializers.CharField(max_length=50)
    user_type = serializers.CharField(max_length=15)


class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

class DailySnacksSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailySnacks
        fields = '__all__'


class CalorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CaloryCount
        fields = '__all__'
