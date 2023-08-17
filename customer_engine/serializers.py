from rest_framework import serializers
from .models import Customer


class SendOtpSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=15)
    user_type = serializers.CharField(max_length=15)

class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'