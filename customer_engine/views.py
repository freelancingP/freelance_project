from .serializers import *
from .models import *
from django.shortcuts import render
from datetime import date
from collections import defaultdict
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
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .common_responce import JsonResponse
import json
from django.db.models import Sum

from django.core.mail import send_mail
import logging
from django.conf import settings


logger = logging.getLogger(__name__)


# Create your views here.
class SendOtpViews(GenericAPIView):
    serializer_class = SendOtpSerializer  # Set the serializer class
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = random.randrange(100000, 999999)
        user_type = serializer.validated_data["user_type"]

        if user_type == "login":
            try:
             
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
                aws_access_key_id = 'AKIASZI2BTK7PJPIYRUN'
                aws_secret_access_key = '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'
                aws_region = 'us-east-2'
                bucket_name = 'fitlife'
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
       
        data = request.data 
         
        try:
            customer = Customer.objects.get(id=request.user.id)
            for key, value in data.items():
                print('key', key, 'values', value)
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
            customer = Customer.objects.get(id=request.user.id)
            try:
                calory_exists = CaloryCount.objects.get(customer=customer)
            except:
                calory_exists = None

            print(calory_exists, ' - ',customer.weight,'',customer.height ,' ', customer.age)
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
                    print(calory_data, 'calory_data')
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
                    print(calory_exists, 'calory_exists')


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
      

class LoginAPIView(APIView):
     
    def post(self, request):
        try:
            serializer_class = SendOtpSerializer
            serializer = serializer_class(data=request.data) 

            if serializer.is_valid():
                validated_data = serializer.validated_data

                contact_number = validated_data.get("country_code") + validated_data.get("phone_number")
                email = validated_data.get("email")
                user_otp = UserOTP.objects.filter(customer__contact_number=contact_number, customer__email=email).last()
                
        
                if user_otp:
                    user_otp.otp = ''.join(random.choices("0123456789", k=6))
                    user_otp.save()
                                    
                    subject = 'Your OTP'
                    message = f'Your OTP is: {user_otp.otp}'
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [email]
                    try:
                        send_mail(subject, message, from_email, recipient_list)
                    except Exception as e:
                        print(f"Error sending email: {e}")          
                                        
                    status_code = status.HTTP_200_OK
                    message = "Success"
                    data = {'otp': user_otp.otp}
                    response = JsonResponse(
                        status=status_code,
                        msg=message,
                        data=data,
                        success=True,
                        error={},
                        count=len(data),
                    )
                    return response

                new_customer = Customer(username=validated_data['email'], email=validated_data['email'], contact_number=contact_number)
                new_customer.save()

                otp = ''.join(random.choices("0123456789", k=6))
                new_user_otp = UserOTP(customer_id=new_customer.id, otp=otp)
                new_user_otp.save()
                
                
                subject = 'Your OTP'
                message = f'Your OTP is: {new_user_otp.otp}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]
                try:
                    send_mail(subject, message, from_email, recipient_list)
                except Exception as e:
                    print(f"Error sending email: {e}")
                    
                status_code = status.HTTP_200_OK
                message = "Success"
                data = {'otp': new_user_otp.otp}
                response = JsonResponse(
                    status=status_code,
                    msg=message,
                    data=data,
                    success=True,
                    error={},
                    count=len(data),
                )
                return response
            
            status_code = status.HTTP_400_BAD_REQUEST
            data = ""
            response = JsonResponse(
                status=status_code,
                data=data,
                success=False,
                error=serializer.errors,
                count=len(data),
            )
            return response
        except Exception as e:
            logger.exception("An error occurred: %s", str(e))

            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal Server Error"
            data = ""
            response = JsonResponse(
                status=status_code,
                msg=message,
                data=data,
                success=False,
                error=str(e),  
                count=len(data),
            )
            return response


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }


class OTPVerifyAPI(APIView):
    def post(self, request):
        try:
            serializer_class = VerifyOtpSerializer
            serializer = serializer_class(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                
                otp = validated_data.get('otp')
                email = validated_data.get('email')
                contact_number = validated_data.get("country_code") + validated_data.get("phone_number")
                user_otp = UserOTP.objects.filter(customer__contact_number=contact_number, customer__email=email).last()

                if user_otp: 
                    if int(user_otp.otp) == int(otp):
                        token = get_tokens_for_user(user_otp.customer)
                        customer_serializer = CustomerSerializer(user_otp.customer)

                        status_code = status.HTTP_200_OK
                        message = "OTP verification successful"

                        token_data = {'token': token["access"]}
                        customer_data = customer_serializer.data 
                        data = {**token_data, **customer_data}    
                        response = JsonResponse(
                            status=status_code,
                            msg=message,
                            data=data,
                            success=True,
                            error={},
                            count=len(data),
                        )
                        return response

                    else:
                        status_code = status.HTTP_400_BAD_REQUEST
                        data = ""
                        response = JsonResponse(
                            status=status_code,
                            msg="Error",
                            data=data,
                            success=False,
                            error="Invalid OTP",
                            count=len(data),
                        )
                        return response
                else:
                    status_code = status.HTTP_400_BAD_REQUEST
                    data = ""
                    response = JsonResponse(
                        status=status_code,
                        msg="Error",
                        data=data,
                        success=False,
                        error="User not found",
                        count=len(data),
                    )
                    return response
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                data = ""
                response = JsonResponse(
                    status=status_code,
                    msg="Error",
                    data=data,
                    success=False,
                    error="Both Email, Phone Number and OTP are required",
                    count=len(data),
                )
                return response

        except Exception as e:
            logger.exception("An error occurred: %s", str(e))

            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal Server Error"
            data = ""
            response = JsonResponse(
                status=status_code,
                msg=message,
                data=data,
                success=False,
                error=str(e),
                count=len(data),
            )
            return response
        

class AllDishesViewSet(viewsets.ModelViewSet):

    queryset = DailySnacks.objects.all()
    serializer_class = DailySnacksSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['meal_type','food', 'dish']
    search_fields = ['meal_type','food']   
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        # Get the user's preference
        customer = self.request.user

        # Filter the queryset based on the selected preference
        queryset = DailySnacks.objects.filter(veg_nonveg_egg__contains=str(customer.veg_nonveg).strip())
        return queryset

    # def get(self, request): 
    #     try:

    #         queryset = self.filter_queryset(self.get_queryset())
    #         page = self.paginate_queryset(queryset)

    #         if page is not None:
    #             serializer = self.get_serializer(page, many=True)
    #             status_code = status.HTTP_200_OK
    #             message = "successful"
    #             data = {"dishes": serializer.data}
    #             response = JsonResponse(
    #                 status=status_code,
    #                 msg=message,
    #                 data=data,
    #                 success=True,
    #                 error={},
    #                 count=len(data),
    #             )
    #             return response
    #         else:
    #             status_code = status.HTTP_400_BAD_REQUEST
    #             data = ""
    #             response = JsonResponse(
    #                 status=status_code,
    #                 msg="Error",
    #                 data=data,
    #                 success=False,
    #                 error="Invalid token",
    #                 count=len(data),
    #             )
    #             return response

    #     except Exception as e:
    #         logger = logging.getLogger(__name__)
    #         logger.exception("An error occurred: %s", str(e))

    #         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    #         message = "Internal Server Error"
    #         data = ""
    #         response = JsonResponse(
    #             status=status_code,
    #             msg=message,
    #             data=data,
    #             success=False,
    #             error=str(e),
    #             count=len(data),
    #         )
    #         return response
            
        
class DailyCaloryView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request, format=None):
        try:
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
                status_code = status.HTTP_200_OK
                serializer = DailySnacksSerializer(data=daily_totals)
                if serializer.is_valid():
                    serializer.save()
                message = "successful"
                data = {"daily_calories": daily_totals}
                response = JsonResponse(
                    status=status_code,
                    msg=message,
                    data=data,
                    success=True,
                    error={},
                    count=len(data),
                )
                return response
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                data = ""
                response = JsonResponse(
                    status=status_code,
                    msg="Error",
                    data=data,
                    success=False,
                    error="No data found for the given meal type",
                    count=len(data),
                )
                return response

        except Exception as e:
            logger.exception("An error occurred: %s", str(e))

            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal Server Error"
            data = ""
            response = JsonResponse(
                status=status_code,
                msg=message,
                data=data,
                success=False,
                error=str(e),
                count=len(data),
            )
            return response


class AddCaloryViews(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        try:

            customer = request.user.id
            
            """
            payload = {
                "dish_ids": [21,33,4]
                
            }
            """
            
            data = request.data
            given_dish_ids = set(data.get("dish_ids", []))


            existing_dish_ids = set(UserSnacks.objects.filter(customer=customer, updated_at__date=date.today()).values_list('dish_id', flat=True))

            dish_ids_to_add = given_dish_ids - existing_dish_ids

            dish_ids_to_remove = existing_dish_ids - given_dish_ids
            
            UserSnacks.objects.filter(customer=customer, dish_id__in=dish_ids_to_remove, updated_at__date=date.today()).delete()

            save_calories = []
            for row in dish_ids_to_add:
                save_calories.append({
                    "customer":customer,
                    "dish":row
                })

            serializer = AddCalorySerializer(data=save_calories, many=True)
            if serializer.is_valid():
                serializer.save()
                status_code = status.HTTP_200_OK
                message = "successful"
                data = JsonResponse(
                    status=status_code,
                    msg=message,
                    data=data,
                    success=True,
                    error={},
                    count=len(data),
                )
                return data
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                data = ""
                response = JsonResponse(
                    status=status_code,
                    msg="Error",
                    data=data,
                    success=False,
                    error="Invalid data",
                    count=len(data),
                )
                return response

        except Exception as e:
            logger.exception("An error occurred: %s", str(e))

            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal Server Error"
            data = ""
            response = JsonResponse(
                status=status_code,
                msg=message,
                data=data,
                success=False,
                error=str(e),
                count=len(data),
            )
            return response

def utils_get_bmi(customer):

    total_calory = 0

    try:

        try:
            if customer.height_unit == 'feet':

                customer.height = customer.height * 30.48

            if customer.weight_unit != 'kg':
                
                customer.weight = customer.weight * 0.453592
        except:
            pass

        bmi_cal = float(customer.weight) / (float(customer.height) * float(customer.height) / 10000)
        fat_cal = (bmi_cal + 3) / 100
        ffm_cal = 1 - fat_cal
        if customer.gender == "Male":
            calory = 88.362+(float(customer.weight)*13.37)+(float(customer.height)*4.799)-(float(customer.age)*5.677)
            total_calory = round((calory * ffm_cal), 0)
        elif customer.gender == "Female":
            calory = 447.593+(float(customer.weight)*9.247)+(float(customer.height)*3.098)-(float(customer.age)*4.33)
            total_calory = round((calory * ffm_cal), 0)
    except:
        pass

    return total_calory

class CustomerDailyCaloriesView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request, date, *args, **kwargs):
        try:

            customer = request.user
            total_calory = utils_get_bmi(customer)
            
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()  

            dish_ids_list = UserSnacks.objects.filter(customer=request.user.id, updated_at__date=date_obj).values_list('dish_id', flat=True)
    
            daily_snacks = DailySnacks.objects.filter(id__in=dish_ids_list)

            total_cals = 0
            total_proteins = 0
            total_carbs = 0
            total_fats = 0
            total_gl = 0

            data = {
                'calories_used':0,
                'total_calory':total_calory,
                'calorie_breakdown':None,
                'breakfast':[],
                'lunch':[],
                'dinner':[],
                'evening_snacks':[],
                'added_dish':dish_ids_list
            }

            for instance in daily_snacks:
                data[instance.meal_type].append({
                            "id": instance.id,
                            "food": instance.food,
                            "ingredients": instance.ingredients,
                            "cals": instance.cals,
                        })
                if instance.cals:
                    total_cals += instance.cals

                if instance.pral:
                    total_proteins += instance.pral

                if instance.carbs:
                    total_carbs += instance.carbs

                if instance.total_fat:
                    total_fats += instance.total_fat
 
                if instance.calcium:
                    total_gl += instance.gl
 
            # update data
            calorie_breakdown = {
                "proteins": {
                        'value':total_proteins,
                        'color':'#2CA3FA',
                        'percentage': 1                
                    },
                "carbs": {
                        'value':total_carbs,
                        'color':'#FF7326',
                        'percentage': 2
                    },
                "fats": {
                        'value':total_fats,
                        'color':'#81BE00',
                        'percentage': 3
                    },
                "gl": {
                    'value':total_gl,
                    'color':'#81BE00',
                    'percentage': 3
                }
            }

            data['calorie_breakdown'] = calorie_breakdown
            data['calories_used'] = total_cals
            data['total_calory'] = total_calory

            status_code = status.HTTP_200_OK
            message = "successful"

            data = JsonResponse(
                    status=status_code,
                    msg=message,
                    data=data,
                    success=True,
                    error={},
                    count=len(data),
                )
            print(data,'---')
            
            return data
        
        except Exception as e:
                logger.exception("An error occurred: %s", str(e))

                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                message = "Internal Server Error"
                response_data = {
                    "status": status_code,
                    "msg": message,
                    "data": {},
                    "success": False,
                    "error": str(e),
                    "count": 0,
                }
                print(data,'-error--')

                return JsonResponse(**response_data)
        

class CalorigramView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        try:
            daily_snacks = DailySnacks.objects.get(id=id)

            data_is = DailySnacksSerializer(daily_snacks).data

            nutrition_value = [
                {"label": "calories", "value": data_is['cals'], "percentage": 5, "color_code": "#01BA91","unit":"cals"},
                {"label": 'glycemic load', "value": data_is['gl'], "percentage": 6, "color_code": "#00AE4D","unit":"gl"},
                {"label": "carbs", "value": data_is['carbs'], "percentage": 3, "color_code": "#29B6C7","unit":"carbs"},
                {"label": "protein", "value": data_is['pral'], "percentage": 5, "color_code": "#98C71C","unit":"pral"},
                {"label": "fats", "value": data_is['total_fat'], "percentage": 5, "color_code": "#E35F11","unit":"fats"},
                {"label": "oil", "value": data_is['oil'], "percentage": 5, "color_code": "#E3B523","unit":"oil"},
            ]

            data = {
                "dish_name": data_is['food'],
                "calories": data_is['cals'],
                "recipes": [ingredient.strip() for ingredient in data_is['ingredients'].split(',')] if data_is['ingredients'] else [],
                "nutrition_value": nutrition_value,
            }

            status_code = status.HTTP_200_OK
            message = "successful"
            response = JsonResponse(
                status=status_code,
                message=message,
                data=data,
                success=True,
                error={},
                count=len(data),
            )
            return response

        except DailySnacks.DoesNotExist:
            logger.error("Daily snacks with ID %s not found", id)

            status_code = status.HTTP_404_NOT_FOUND
            message = "Daily snacks not found"
            response = JsonResponse(
                status=status_code,
                message=message,
                data=[],
                success=True,
                error="Daily snacks not found",
                count=len(""),
            )
            return response

        except Exception as e:
            logger.exception("An error occurred while processing the request: %s", str(e))

            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal Server Error"
            response_data = {
                "status": status_code,
                "message": message,
                "data": {},
                "success": False,
                "error": str(e),
                "count": 0,
            }
            return JsonResponse(response_data, status=status_code)


class CreateRecipe(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request, format=None):
        try:
            serializer = RecipeSerializer(data=request.data)

            if serializer.is_valid():
                recipe = serializer.save()

                ingredients_data = request.data.get('ingredients', [])
                for ingredient_data in ingredients_data:
                    ingredient_data['recipe'] = recipe.id
                    ingredient_serializer = RecipeIngridientSerializer(data=ingredient_data)
                    if ingredient_serializer.is_valid():
                        ingredient_serializer.save()
                    else:
                        logger.error("Error while saving ingredient: %s", ingredient_serializer.errors)

                        status_code = status.HTTP_400_BAD_REQUEST
                        message = "Bad request"
                        response = JsonResponse(
                            status=status_code,
                            message=message,
                            data=[],
                            success=True,
                            error=ingredient_serializer.errors,
                            count=len(ingredient_serializer.errors),
                        )
                        return response

                status_code = status.HTTP_201_CREATED
                message = "successful"
                data = JsonResponse(
                        status=status_code,
                        msg=message,
                        data=serializer.data,
                        success=True,
                        error={},
                        count=len("data"),
                    )
                return data

            status_code = status.HTTP_400_BAD_REQUEST
            message = "Bad request"
            response = JsonResponse(
                status=status_code,
                message=message,
                data=[],
                success=True,
                error=serializer.errors,
                count=len(serializer.errors),
            )
            return response

        except Exception as e:
            logger.exception("An error occurred while processing the request: %s", str(e))

            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal Server Error"
            response_data = {
                "status": status_code,
                "message": message,
                "data": {},
                "success": False,
                "error": str(e),
                "count": 0,
            }
            return JsonResponse(response_data, status=status_code)

    
class DailyCalorigramView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request, date, *args, **kwargs):
        try:
            customer = request.user
            meal_type = request.query_params.get('meal_type')
            date_obj = datetime.strptime(date, "%Y-%m-%d").date() 
            user_snacks_filter = {'customer': customer.id, 'updated_at__date': date_obj}

            all_data = []
            if meal_type:
                all_data = DailySnacks.objects.filter(meal_type=meal_type)
            else:
                all_data = DailySnacks.objects.all()
                
            dish_ids_list = UserSnacks.objects.filter(**user_snacks_filter).values_list('dish_id', flat=True)
            data_is = DailySnacksSerializer(all_data, many=True).data
            
            meal_types = ["breakfast", "lunch", "evening_snacks", "dinner"]
            eaten_calories_breakdown = {meal_type: 0 for meal_type in meal_types}

            eaten_calories = 0
            remaining_calories = 1

            eaten_gl = 0
            remaining_gl = 1

            eaten_carbs = 0
            remaining_carbs = 1 

            eaten_pral = 0
            remaining_pral = 1

            eaten_total_fat = 0
            remaining_total_fat = 1

            eaten_oil = 0
            remaining_oil = 1

            for item in data_is:
                if item['id'] in dish_ids_list:
                    meal_type = item['meal_type'].lower()
                    eaten_calories_breakdown[meal_type] += item['cals']

                    if item['gl'] is not None:
                        eaten_gl += item['gl']

                    eaten_carbs += item['carbs']
                    eaten_pral += item['pral']
                    eaten_total_fat += item['total_fat']
                    eaten_oil += item['oil']

                    eaten_calories += item['cals']
                else:
                    remaining_calories += item['cals']
                    remaining_gl += item['gl']
                    remaining_carbs += item['carbs']
                    remaining_pral += item['pral']
                    remaining_total_fat += item['total_fat']
                    remaining_oil += item['oil']

            nutrition_value = [
                {"label": "calories", "value": eaten_calories, "percentage": round(eaten_calories / (eaten_calories + remaining_calories) * 100) if eaten_calories + remaining_calories > 0 else 0, "color_code": "#01BA91", "unit": "cals"},
                {"label": 'glycemic load', "value": eaten_gl, "percentage": round(eaten_gl / (eaten_gl + remaining_gl) * 100) if eaten_gl + remaining_gl > 0 else 0, "color_code": "#00AE4D", "unit": "gl"},
                {"label": "carbs", "value": eaten_carbs, "percentage": round(eaten_carbs / (eaten_carbs + remaining_carbs) * 100) if eaten_carbs + remaining_carbs > 0 else 0, "color_code": "#29B6C7", "unit": "carbs"},
                {"label": "protein", "value": eaten_pral, "percentage": round(eaten_pral / (eaten_pral + remaining_pral) * 100) if eaten_pral + remaining_pral > 0 else 0, "color_code": "#98C71C", "unit": "pral"},
                {"label": "fats", "value": eaten_total_fat, "percentage": round(eaten_total_fat / (eaten_total_fat + remaining_total_fat) * 100) if eaten_total_fat + remaining_total_fat > 0 else 0, "color_code": "#E35F11", "unit": "fats"},
                {"label": "oil", "value": eaten_oil, "percentage": round(eaten_oil / (eaten_oil + remaining_oil) * 100) if eaten_oil + remaining_oil > 0 else 0, "color_code": "#E3B523", "unit": "oil"},
            ]

            total_calory = utils_get_bmi(customer)

            data = {
                'eaten_calories': eaten_calories,
                'remaining_calories': total_calory,
                'eaten_calories_breakdown': eaten_calories_breakdown,
                'nutrition_value': nutrition_value
            }

            status_code = status.HTTP_200_OK
            message = "successful"
            response = JsonResponse(
                status=status_code,
                message=message,
                data=data,
                success=True,
                error={},
                count=len(data),
            )
            return response

        except ValueError as ve:
            logger.exception("ValueError occurred while processing the request: %s", str(ve))

            status_code = status.HTTP_400_BAD_REQUEST
            message = "Invalid date format"
            response = JsonResponse(
                status=status_code,
                message=message,
                data=None,
                success=False,
                error={},
                count=0,
            )
            return response

        except Exception as e:
            logger.exception("An error occurred while processing the request: %s", str(e))

            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal Server Error"
            response_data = {
                "status": status_code,
                "message": message,
                "data": {},
                "success": False,
                "error": str(e),
                "count": 0,
            }
            return JsonResponse(response_data, status=status_code)


class GetIngridientView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request, id=None, *args, **kwargs):
        try:
            if id is not None:
                try:
                    dish = Dishes.objects.get(id=id)
                    data = {"name": dish.food}
                    status_code = status.HTTP_200_OK
                    message = "successful"
                    response = JsonResponse(
                        status=status_code,
                        message=message,
                        data=data,
                        success=True,
                        error={},
                        count=len(data),
                    )
                    return response
                except Dishes.DoesNotExist:
                    status_code = status.HTTP_400_BAD_REQUEST
                    message = "Dish not found"
                    response = JsonResponse(
                        status=status_code,
                        message=message,
                        data=None,
                        success=False,
                        error={},
                        count=0,
                    )
                    return response
            else:
                dishes = Dishes.objects.all()
                data = [{"id": dish.id, "name": dish.food} for dish in dishes]
                status_code = status.HTTP_200_OK
                message = "successful"
                response = JsonResponse(
                    status=status_code,
                    message=message,
                    data=data,
                    success=True,
                    error={},
                    count=len(data),
                )
                return response

        except Exception as e:
            logger.exception("An error occurred while processing the request: %s", str(e))

            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = "Internal Server Error"
            response_data = {
                "status": status_code,
                "message": message,
                "data": {},
                "success": False,
                "error": str(e),
                "count": 0,
            }
            return JsonResponse(response_data, status=status_code)


class UserProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_day_of_week(self, date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        print(date_str, date_obj.strftime('%A'))
        return date_obj.strftime('%A')
        
    
    def get(self, request, *args, **kwargs):
        customer = request.user
        try:
            user_profile = Customer.objects.get(id=customer.id)
        except Customer.DoesNotExist as customer_does_not_exist_error:
            logger.error("Customer with ID %s does not exist: %s", customer.id, str(customer_does_not_exist_error))
            response = JsonResponse(
                {"detail": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
                message="Customer not found",
                data=None,
                success=False,
                error={},
                count=0,
            )
            return response

        operation_type = request.query_params.get('type', 'weekly')
        selected_days = None
        if operation_type == 'weekly':
            selected_days = timezone.now() - timedelta(days=7)

        dish_ids_list = UserSnacks.objects.filter(
                customer=customer,
                updated_at__date__gte=(selected_days.date()),
                updated_at__date__lt=(timezone.now().date())
            )
        
        dates = []
        for i in range(7):
            current_date = selected_days + timedelta(days=i)
            date_str = str(current_date.date())
            dates.insert(current_date.weekday(), date_str)

        date_dish_dict = {}
        for row in dates:
            date_dish_dict[row] = []

        for user_snack in dish_ids_list:

            updated_at = str(user_snack.updated_at.date())
            dish_id = user_snack.dish_id

            if updated_at in date_dish_dict:
                date_dish_dict[updated_at].append(dish_id)
            else:
                date_dish_dict[updated_at] = [dish_id]
        
        for date_str in date_dish_dict.keys():
            if not date_dish_dict[date_str]:
                date_dish_dict[date_str] = []

        cals = []
        sodium = []
        pral = []
        oil = []
        gl = []
        aaf_adj_prot = []
        carbs = []
        total_fat = []
        tdf = []
        potassium = []
        phosphorus = []
        calcium = []
        magnesium = []
        total_eaa = []
        lysine = []
        gross_protein = []
        free_sugar = []
        aa_factor = []
        glucose = []

        column_names = [
            'cals', 'sodium', 'pral', 'oil', 'gl', 'aaf_adj_prot', 'carbs', 'total_fat', 'tdf',
            'potassium', 'phosphorus', 'calcium', 'magnesium', 'total_eaa', 'lysine',
            'gross_protein', 'free_sugar', 'aa_factor', 'glucose',
        ]

        for date, dish_ids in date_dish_dict.items():
            data_queryset = DailySnacks.objects.filter(id__in=dish_ids).values(*column_names)

            data_summary = (
                data_queryset
                .aggregate(
                    total_cals=Sum('cals'),
                    total_sodium=Sum('sodium'),
                    total_pral=Sum('pral'),
                    total_oil=Sum('oil'),
                    total_gl=Sum('gl'),
                    total_aaf_adj_prot=Sum('aaf_adj_prot'),
                    total_carbs=Sum('carbs'),
                    total_total_fat=Sum('total_fat'),
                    total_tdf=Sum('tdf'),
                    total_potassium=Sum('potassium'),
                    total_phosphorus=Sum('phosphorus'),
                    total_calcium=Sum('calcium'),
                    total_magnesium=Sum('magnesium'),
                    total_total_eaa=Sum('total_eaa'),
                    total_lysine=Sum('lysine'),
                    total_gross_protein=Sum('gross_protein'),
                    total_free_sugar=Sum('free_sugar'),
                    total_aa_factor=Sum('aa_factor'),
                    total_glucose=Sum('glucose')
                )
            )    
            
            cals.append(data_summary['total_cals'] or 0)
            sodium.append(data_summary['total_sodium'] or 0)
            pral.append(data_summary['total_pral'] or 0)
            oil.append(data_summary['total_oil'] or 0)
            gl.append(data_summary['total_gl'] or 0)
            aaf_adj_prot.append(data_summary['total_aaf_adj_prot'] or 0)
            carbs.append(data_summary['total_carbs'] or 0)
            total_fat.append(data_summary['total_total_fat'] or 0)
            tdf.append(data_summary['total_tdf'] or 0)
            potassium.append(data_summary['total_potassium'] or 0)
            phosphorus.append(data_summary['total_phosphorus'] or 0)
            calcium.append(data_summary['total_calcium'] or 0)
            magnesium.append(data_summary['total_magnesium'] or 0)
            total_eaa.append(data_summary['total_total_eaa'] or 0)
            lysine.append(data_summary['total_lysine'] or 0)
            gross_protein.append(data_summary['total_gross_protein'] or 0)
            free_sugar.append(data_summary['total_free_sugar'] or 0)
            aa_factor.append(data_summary['total_aa_factor'] or 0)
            glucose.append(data_summary['total_glucose'] or 0)

        if len(cals) > 0:
            average_calorie = sum(cals) / len(cals)
        else:
            average_calorie = 0
        
        data_points = []
        for column_name in column_names:
            data_points.append({
                "name": column_name, 
                "values": eval(column_name),
            })


        response_data = {
            "user_image": user_profile.image_url,
            "name": f"{user_profile.first_name} {user_profile.last_name}",
            "age": user_profile.age,
            "calories": round(sum(cals), 2),
            "calorie_intake": {
                "average_calorie": round(average_calorie, 2),
                "data_points": cals,
            },
            "nutrition_intake": {
                "data_points":data_points
            }
        }

        status_code = status.HTTP_200_OK
        message = "successful"
        response = JsonResponse(
            status=status_code,
            message=message,
            data=response_data,
            success=True,
            error={},
            count=len(response_data),
        )
        return response
    

class UserProfileDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        customer = request.user
        try:
            user_profile = Customer.objects.get(id=customer.id)
        except Customer.DoesNotExist as customer_does_not_exist_error:
            logger.error("Customer with ID %s does not exist: %s", customer.id, str(customer_does_not_exist_error))
            response = JsonResponse(
                {"detail": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
                message="Customer not found",
                data=None,
                success=False,
                error={},
                count=0,
            )
            return response

        serializer = CustomerSerializer(instance=user_profile)
     
        total_calory = utils_get_bmi(customer)

        data = serializer.data
        data['calories'] = total_calory 
        status_code = status.HTTP_200_OK
        message = "successful"
        response = JsonResponse(
            status=status_code,
            message=message,
            data=data,
            success=True,
            error={},
            count=len(data),
        )
        return response