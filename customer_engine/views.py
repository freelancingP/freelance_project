from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import json
from .serializers import CustomerSerializer, SendOtpSerializer,VerifyOtpSerializer
from django.http import Http404
from rest_framework.generics import GenericAPIView
from datetime import datetime, timedelta
import jwt

# Create your views here.


class SendOtpViews(GenericAPIView):
    serializer_class = SendOtpSerializer  # Set the serializer class

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = random.randrange(100000, 999999)
        
        user_type = serializer.validated_data["user_type"]
        print(user_type)
        if user_type == "login":
            try:
                customer = Customer.objects.get(contact_number=serializer.validated_data["number"])
                user_data = UserOTP(user = customer, otp = otp)
                user_data.save()
                response_data = {
                    "data": {
                        "number": customer.contact_number,
                        "otp": otp,
                    },
                    "status": True,
                    "code": 200,
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
                customer = Customer.objects.get(contact_number=serializer.validated_data["number"])
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
                data = Customer(image = None, first_name = None, last_name = None ,gender = None,location = None, address = None, contact_number = serializer.validated_data["number"],email = None, date_of_birth = None, age = None , height = None, weight = None, health_issue = None, other_issue = None, any_medication = None, veg_nonveg = None, profession = None , help=None)
                data.save()
                customer = Customer.objects.get(contact_number=serializer.validated_data["number"])
                user_data = UserOTP(user = customer, otp = otp)
                user_data.save()
                response_data = {
                    "data": {
                        "number": serializer.validated_data["number"],
                        "otp": otp,
                    },
                    "status": True,
                    "code": 200,
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

class UpdateUserDetailViews(GenericAPIView):
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
                    serializer = CustomerSerializer(customer)
                    response_data ={
                        "data": serializer.data,
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

