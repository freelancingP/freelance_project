from rest_framework import serializers
from .models import Customer


class SendOtpSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=15)
    user_type = serializers.CharField(max_length=15)

class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    

class CustomListField(serializers.ListField):
    def to_representation(self, data):
        if isinstance(data, str):
            return [item.strip() for item in data.split(',')]
        return data

class CustomerSerializer(serializers.ModelSerializer):
    health_issue = CustomListField()
    other_issue = CustomListField()

    class Meta:
        model = Customer
        fields = '__all__'