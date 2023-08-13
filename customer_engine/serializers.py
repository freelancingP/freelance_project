from rest_framework import serializers
from .models import Customer


class SendOtpSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=15)
    user_type = serializers.CharField(max_length=15)

class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    

class CustomerSerializer(serializers.ModelSerializer):
    # Define a read-only field for the S3 bucket image URL
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'

    def get_image_url(self, obj):
        # Replace 'appstacklabs' with your actual S3 bucket name
        bucket_name = 'appstacklabs'
        image_name = obj.image.name.split('/')[-1]  # Extract the image file name
        image_url = f'https://appstacklabs.s3.us-east-2.amazonaws.com/images/{image_name}'
        print(image_url)
        return image_url