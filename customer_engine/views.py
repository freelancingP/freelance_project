from .serializers import *
from .models import *
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import json
from .serializers import *
from django.http import Http404
from rest_framework.generics import GenericAPIView
from datetime import datetime, timedelta
import boto3
from rest_framework.parsers import MultiPartParser, FileUploadParser
import io
from .decorators import *
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer, DailySnacks
from .serializers import DailySnacksSerializer
import jwt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.authtoken.models import Token


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            # Check if a user with the provided username already exists
            existing_user = UserProfile.objects.filter(username=validated_data['username']).first()
            
            if existing_user:
                # Generate and save a new OTP for the existing user
                existing_user.otp = ''.join(random.choices("0123456789", k=6))
                existing_user.save()
                
                # Get or create an authentication token for the user
                token_obj = Token.objects.get_or_create(user=existing_user)

                
                # Include the authentication token in the response
                return Response({'otp': existing_user.otp, 'token': str(token_obj)}, status=status.HTTP_200_OK)

            # Create a new user
            new_user = UserProfile(username=validated_data['username'], email=validated_data['email'])
            new_user.otp = ''.join(random.choices("0123456789", k=6))
            new_user.save()
            
            # Get or create an authentication token for the new user
            token_obj = Token.objects.get_or_create(user=new_user)
            
            # Include the authentication token in the response
            return Response({'otp': new_user.otp, 'token': str(token_obj)}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class OTPVerifyAPI(APIView):
    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        username = request.data.get('username')
        
        if not otp or not username:
            return Response({'error': 'Both username and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if user.otp == int(otp):
            
            return Response({'message': 'OTP verification successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
class SendOtpViews(GenericAPIView):
    serializer_class = SendOtpSerializer  # Set the serializer class
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = random.randrange(100000, 999999)
        print(serializer.validated_data)
        
        user_type = serializer.validated_data["user_type"]
        print(user_type)
        if user_type == "login":
            try:
              print("uiho")
              contact_number = serializer.validated_data.get("country_code") + serializer.validated_data.get("phone_number")
              email = serializer.validated_data.get("email")
              customer = Customer.objects.filter(Q(contact_number=contact_number) | Q(email=email)).first()
              if customer:
                  print(customer)
                  user_data = UserOTP(user = customer, otp = otp)
                  print(customer.contact_number)
                  user_data.save()
                  numbers = "91" + customer.contact_number
                  response_data = {
                      "data": {
                          "number": customer.contact_number,
                          "email": customer.email,
                          "otp": otp,
                      },
                      "status": True,
                      "code": 200,
                  }
                  return Response(response_data)
              else:
                response_data = {
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "User Not Registered.",
                }
                return Response(response_data)
            except Customer.DoesNotExist:
                response_data = {
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "User Not Registered.",
                }
                return Response(response_data)
        else:
            try:
                contact_number = serializer.validated_data.get("country_code") + serializer.validated_data.get("phone_number")
                email = serializer.validated_data.get("email")
                customer = Customer.objects.filter(Q(contact_number=contact_number) | Q(email=email)).exists()
            except:
                customer = None
            if customer:
                response_data = {
                  "data": None,
                  "status": False,
                  "code": 401,
                  "message": "User already exists."
                }
                return Response(response_data)
            else:
                contact_number = serializer.validated_data["country_code"] + serializer.validated_data["phone_number"]
                data = Customer(image_url=None, first_name=None, last_name=None, gender=None, location=None, address=None, contact_number=contact_number, email=serializer.validated_data["email"], date_of_birth=None, age=None, height=None, height_unit=None, weight_unit=None, weight=None, health_issue=None, other_issue=None, any_medication=None, veg_nonveg=None, profession=None, help=None)
                data.save()
                try:
                  customer = Customer.objects.get(Q(contact_number=contact_number) | Q(email=serializer.validated_data["email"]))
                  user_data = UserOTP(user=customer, otp=otp)
                  user_data.save()
                  print("juwe")
                  response_data = {
                      "data": {
                          "phone_number": customer.contact_number,
                          "email": customer.contact_number,
                          "otp": otp,
                      },
                      "status": True,
                      "code": 200,
                  }
                  return Response(response_data)
                except Exception as e:
                  print(e)
                  response_data = {
                      "data": None,
                      "message":"Provide Correct Input Key Value Paire",
                      "status": False,
                      "code": 400,
                  }
                  return Response(response_data)

class VerifyOtpViews(GenericAPIView):
    serializer_class = VerifyOtpSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        try:
            otp = UserOTP.objects.get(otp= serializer.validated_data["otp"])
        except:
            otp = None
        if otp:
            otp.delete()         
            customer = Customer.objects.get(contact_number=otp.user.contact_number)
            print(customer)
            access_token_expiry = datetime.utcnow() + timedelta(minutes=30)
            refresh_token_expiry = datetime.utcnow() + timedelta(minutes=30)
            # Generate the access token
            access_token_payload = {
                'client_id': customer.contact_number,
                'exp': access_token_expiry,
                'iat': datetime.utcnow(),
            }
            access_token = jwt.encode(access_token_payload, str(customer.id), algorithm='HS256')
            # Generate the refresh token
            refresh_token_payload = {
                'client_id': customer.email,
                'exp': refresh_token_expiry,
                'iat': datetime.utcnow(),
            }
            refresh_token = jwt.encode(refresh_token_payload, customer.contact_number, algorithm='HS256')
            print(access_token)
            print(refresh_token)
            # Serialize the customer object
            serializer = CustomerSerializer(customer)
            response_data = {
                "data": {
                    "accessToken": access_token,
                    "user":serializer.data
                },
                "status": True,
                "code": 200
            }
            return Response(response_data)
        else:
            response_data ={
                "data": None,
                "status": False,
                "code": 401,
                "message": "Invalid OTP.",
            }
            return Response(response_data)

class UploadImageView(GenericAPIView):
    parser_classes = [MultiPartParser]  # Allow file uploads
    
    def post(self, request):
        data = request.data
        print(data)

        try:
            uploaded_image = request.data.get("image")
            print(uploaded_image)
            if uploaded_image:
                uploaded_image = data["image"]
                aws_access_key_id = 'AKIAU62W7KNUZ4DKGRU3'
                aws_secret_access_key = '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'
                aws_region = 'us-east-2'
                bucket_name = 'appstacklabs'
                s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
                object_key = f"images/{uploaded_image}"  # Adjust the path in the bucket as needed
                image_data = uploaded_image.read()
                # Upload the image data to S3 using put_object
                s3.put_object(Body=image_data, Bucket=bucket_name, Key=object_key)
                s3_image_url = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{object_key}"
                print(s3_image_url)
                response_data = {
                    "data": s3_image_url,
                    "status": True,
                    "code": 200,
                    "message": "Image Successfully uploaded.",
                }
                return Response(response_data)
            else:
                response_data ={
                "data": None,
                "status": False,
                "code": 400,
                "message": "Image Not Found.",
            }
        except Exception as e:
            print(e)
            response_data ={
                "data": None,
                "status": False,
                "code": 500,
                "message": "Something Wrong, Try again.",
            }
            return Response(response_data)
    




class UpdateUserDetailViews(APIView):   
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        data = request.data
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            try:
                decoded_payload = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})
                try:
                    customer = Customer.objects.get(contact_number=decoded_payload['client_id'])
                    for key, value in data.items():
                        if isinstance(value, list):
                            value = ', '.join(value)  # Convert list to comma-separated string
                        if hasattr(customer, key):
                            setattr(customer, key, value)
                        else:
                            response_data ={
                                "data": None,
                                "status": False,
                                "code": 400,
                                "message": f"Invalid field name: {key}",
                            }
                            return Response(response_data)
                    customer.save()
                    customer = Customer.objects.get(contact_number=decoded_payload['client_id'])
                    try:
                      calory_exists = CaloryCount.objects.get(customer=customer)
                    except:
                      calory_exists = None
                    if calory_exists is None:
                      if customer.weight is not None and customer.height is not None and customer.age is not None:
                        if customer.gender == "Male":
                            calory = 88.362+(float(customer.weight)*13.37)+(float(customer.height)*4.799)-(float(customer.age)*5.677)
                            total_calory = round((calory * 0.702050619834711),2)
                        elif customer.gender == "Female":
                            calory = 447.593+(float(customer.weight)*9.247)+(float(customer.height)*3.098)-(float(customer.age)*4.33)
                            total_calory = round((calory * 0.702050619834711),2)
                        else:
                          total_calory = 0.0
                        calory_data = CaloryCount(customer=customer,total_calory=total_calory)
                        calory_data.save()
                    else:
                      if customer.weight is not None and customer.height is not None and customer.age is not None:
                        if customer.gender == "Male":
                            calory = 88.362+(float(customer.weight)*13.37)+(float(customer.height)*4.799)-(float(customer.age)*5.677)
                            total_calory = round((calory * 0.702050619834711),2)
                        elif customer.gender == "Female":
                            calory = 447.593+(float(customer.weight)*9.247)+(float(customer.height)*3.098)-(float(customer.age)*4.33)
                            total_calory = round((calory * 0.702050619834711),2)
                        else:
                          total_calory = 0.0
                        calory_exists.total_calory = total_calory
                        calory_exists.save()

                    serializer = CustomerSerializer(customer)
                    serialized_data = serializer.data

                    response_data = {
                        "data": serialized_data,
                        "status": True,
                        "code": 200,
                        "message": "User Detail Successfully updated.",
                    }
                    return Response(response_data)
                    
                except Customer.DoesNotExist:
                    response_data ={
                        "data": None,
                        "status": False,
                        "code": 401,
                        "message": "User Doesn't exist.",
                    }
                    return Response(response_data)
                except Exception as e:
                    print(e)
                    response_data ={
                        "data": None,
                        "status": False,
                        "code": 500,
                        "message": "An error occurred.",
                    }
                    return Response(response_data)
            except jwt.ExpiredSignatureError:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "Token has expired.",
                }
                return Response(response_data)
            except jwt.DecodeError:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 498,
                    "message": "Invalid token.",
                }
                return Response(response_data)
        else:
            response_data ={
                "data": None,
                "status": False,
                "code": 400,
                "message": "No token provided.",
            }
            return Response(response_data)



class AllDishesViewSet(viewsets.ModelViewSet):
    queryset = DailySnacks.objects.all()
    serializer_class = DailySnacksSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['meal_type','food']
    search_fields = ['meal_type','food']   
   

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": {"dishes": serializer.data}})
            

class DailyCaloryView(APIView):

    def post(self, request, format=None):
        meal_type = request.data.get('meal_type')
        data_queryset = DailySnacks.objects.filter(meal_type=meal_type)

        if data_queryset.exists():
            data_list = list(data_queryset)

            total_calories = 0.0
            total_carbs = 0.0
            total_proteins = 0.0

            for item in data_list:
                if item.cals is not None:
                    total_calories += item.cals
                if item.carbs is not None:
                    total_carbs += item.carbs
                if item.pral is not None:
                    total_proteins += item.pral

            daily_totals = {
                'calories': total_calories,
                'carbs': total_carbs,
                'proteins': total_proteins,
            }


            return Response(daily_totals, status=status.HTTP_201_CREATED)
        return Response({'error': 'No data found for the given meal type.'}, status=status.HTTP_400_BAD_REQUEST)
    


