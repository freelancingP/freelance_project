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
        if user_type == "SignIn":
            try:
                customer = Customer.objects.get(contact_number=serializer.validated_data["number"])
                access_token_expiry = datetime.utcnow() + timedelta(minutes=30)
                refresh_token_expiry = datetime.utcnow() + timedelta(minutes=30)
                # Generate the access token
                access_token_payload = {
                    'client_id': customer.email,
                    'exp': access_token_expiry,
                    'iat': datetime.utcnow(),
                }
                access_token = jwt.encode(access_token_payload, customer.contact_number, algorithm='HS256')
                # Generate the refresh token
                refresh_token_payload = {
                    'client_id': customer.email,
                    'exp': refresh_token_expiry,
                    'iat': datetime.utcnow(),
                }
                refresh_token = jwt.encode(refresh_token_payload, customer.contact_number, algorithm='HS256')
                print(access_token)
                print(refresh_token)
                

                request.session["customer"] = customer.id
                request.session["c_otp"] = otp
                response_data = {
                    "data": {
                        "token": access_token,
                        "number": customer.contact_number,
                        "otp": otp,
                    },
                    "status": True,
                    "code": 200,
                    "message": "User Registered",
                }
                return Response(response_data)
            except Customer.DoesNotExist:
                response_data = {
                    "data": {
                        "otp":otp
                    },
                    "status": False,
                    "code": 404,
                    "message": "User Not Registered.",
                }
                return Response(response_data)
            except Exception as e:
                response_data = {
                    "data": None,
                    "status": False,
                    "code": 500,
                    "message": "Something went wrong,Please Try Again.",
                }
                return Response(response_data)
        else:
            request.session["phone_number"] = serializer.validated_data["number"]
            request.session["signup_otp"] = otp
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

        user_type = serializer.validated_data["user_type"]
        if user_type == "SignIn":
            try:
                decoded_payload = jwt.decode(serializer.validated_data["token"], algorithms=['HS256'], options={"verify_signature": False})
                try:      
                    otp = request.session.get("c_otp")  # Retrieve and remove the OTP from the session
                    if  str(otp) == serializer.validated_data["otp"]:
                        del request.session["c_otp"]
                        customer_id = request.session.get("customer")
                        if customer_id:
                            try:
                                customer = Customer.objects.get(id=customer_id)

                                # Serialize the customer object
                                serializer = CustomerSerializer(customer)
                                response_data = serializer.data

                                return Response(response_data)
                            except Customer.DoesNotExist:
                                response_data =  {
                                    "data": None,
                                    "status": False,
                                    "code": 404,
                                    "message": "Customer does not exist.",
                                }
                                return Response(response_data)
                        else:
                            response_data = {
                                "data": None,
                                "status": False,
                                "code": 400,
                                "message": "Customer ID not found in the session.",
                            }
                            return Response(response_data)
                    else:
                        response_data ={
                            "data": None,
                            "status": False,
                            "code": 401,
                            "message": "Wrong OTP, Please Enter Correct OTP.",
                        }
                        return Response(response_data)
                except KeyError:
                    response_data = {
                        "data": None,
                        "status": False,
                        "code": 400,
                        "message": "OTP Does not Exist.",
                    }
                    return Response(response_data)
            except jwt.ExpiredSignatureError:
                response_data = {
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "Token has expired.",
                }
                return Response(response_data)
            except jwt.DecodeError:
                response_data = {
                    "data": None,
                    "status": False,
                    "code": 498,
                    "message": "Invalid token.",
                }
                return Response(response_data)
        else:
            otp = request.session["signup_otp"]
            if  str(otp) == serializer.validated_data["otp"]:
                response_data = {
                    "data": {
                        "number": request.session["phone_number"],
                        "otp": otp,
                    },
                    "status": True,
                    "code": 200,
                    "message": "OTP Verified",
                }
                return Response(response_data)
            else:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "Wrong OTP, Please Enter Correct OTP.",
                }
                return Response(response_data)





