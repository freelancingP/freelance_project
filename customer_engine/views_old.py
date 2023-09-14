from django.shortcuts import render
from ..models_old import *
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import json
from .serializers_old import *
from django.http import Http404
from rest_framework.generics import GenericAPIView
from datetime import datetime, timedelta
import jwt
import boto3
from rest_framework.parsers import MultiPartParser, FileUploadParser
import io
from .decorators import *
from django.db.models import Q
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



class AllDishesViews(APIView):   
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        data = request.data
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            try:
                decoded_payload = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})
                try:
                    customer = Customer.objects.get(contact_number=decoded_payload['client_id'])
                    print(customer)
                    try:
                        t_calory = CaloryCount.objects.get(customer=customer)
                        total_calory = t_calory.total_calory
                    except:
                        total_calory = None
                    breakfast_instances = Breakfast.objects.all()  # Retrieve all Breakfast instances
                    breakfastserializer = BreakfastSerializer(breakfast_instances, many=True)
                    breakfast_data_list = breakfastserializer.data

                    breackfast_data = []
                    for data in breakfast_data_list:
                        input_string = data['ingredients']

                        ingredients = input_string.split(",")  # Split the string into a list of ingredients

                        recipe_values = []

                        for ingredient in ingredients:
                            # Assuming you want to create a dictionary with a "name" key and a fixed "quantity" value
                            recipe_values.append({
                                "name": ingredient,
                            })
                        breakfast_item = {
                            "dishId": data['id'],
                            "dishName": data['food'],
                            "ingredients": data['ingredients'],
                            "calories": 400,
                            "nutritionValues": [
                              {
                                "name": data['oil'],
                                "quantity": data['quantity'],
                                "percentage":25,
                                "colour":"#01BA91",
                              },

                            ],
                            "recipeValues": recipe_values
                          }
                        breackfast_data.append(breakfast_item)
                    
                    launch_instances = Lunch.objects.all()  # Retrieve all Launch instances
                    launchserializer = LunchSerializer(launch_instances, many=True)
                    lunch_data_list = launchserializer.data

                    lunch_data = []
                    for data in lunch_data_list:
                        input_string = data['ingredients']

                        ingredients = input_string.split(",")  # Split the string into a list of ingredients

                        recipe_values = []

                        for ingredient in ingredients:
                            # Assuming you want to create a dictionary with a "name" key and a fixed "quantity" value
                            recipe_values.append({
                                "name": ingredient,
                            })
                        lunch_item = {
                            "dishId": data['id'],
                            "dishName": data['food'],
                            "ingredients": data['ingredients'],
                            "calories": 400,
                            "nutritionValues": [
                              {
                                "name": data['oil'],
                                "quantity": data['quantity'],
                                "percentage":25,
                                "colour":"#01BA91",
                              },

                            ],
                            "recipeValues": recipe_values
                          }
                        lunch_data.append(lunch_item)
                    
                    dinner_instances = Dinner.objects.all()  # Retrieve all Dinner instances
                    dinnerserializer = DinnerSerializer(dinner_instances, many=True)
                    dinner_data_list = dinnerserializer.data

                    dinner_data = []
                    for data in dinner_data_list:
                        input_string = data['ingredients']

                        ingredients = input_string.split(",")  # Split the string into a list of ingredients

                        recipe_values = []

                        for ingredient in ingredients:
                            # Assuming you want to create a dictionary with a "name" key and a fixed "quantity" value
                            recipe_values.append({
                                "name": ingredient,
                            })
                        dinner_item = {
                            "dishId": data['id'],
                            "dishName": data['food'],
                            "ingredients": data['ingredients'],
                            "calories": 400,
                            "nutritionValues": [
                              {
                                "name": data['oil'],
                                "quantity": data['quantity'],
                                "percentage":25,
                                "colour":"#01BA91",
                              },

                            ],
                            "recipeValues": recipe_values
                          }
                        dinner_data.append(dinner_item)
                    
                    snacks_instances = Snacks.objects.all()  # Retrieve all Snacks instances
                    snacksserializer = SnacksSerializer(snacks_instances, many=True)
                    snacks_data_list = snacksserializer.data

                    snacks_data = []
                    for data in snacks_data_list:
                        input_string = data['ingredients']

                        ingredients = input_string.split(",")  # Split the string into a list of ingredients

                        recipe_values = []

                        for ingredient in ingredients:
                            # Assuming you want to create a dictionary with a "name" key and a fixed "quantity" value
                            recipe_values.append({
                                "name": ingredient,
                            })
                        snacks_item = {
                            "dishId": data['id'],
                            "dishName": data['food'],
                            "ingredients": data['ingredients'],
                            "calories": 400,
                            "nutritionValues": [
                              {
                                "name": data['oil'],
                                "quantity": data['quantity'],
                                "percentage":25,
                                "colour":"#01BA91",
                              },

                            ],
                            "recipeValues":recipe_values
                          }
                        snacks_data.append(snacks_item)
                    response_data ={
                      "data": {
                        "caloriesUsed": 650,
                        "totalCalory": total_calory,
                        "calorieBreakdown": {
                          "calories": 100,
                          "pral": 100,
                          "calcium": 450
                        },
                        "breakfast": breackfast_data,
                        "lunch": lunch_data,
                        "Snacks": snacks_data,
                        "dinner": dinner_data,
                      }
                    }

                    # print(response_data)
                    return Response(response_data)
                except Customer.DoesNotExist:
                    response_data ={
                        "data": None,
                        "status": False,
                        "code": 401,
                        "message": "Invalid Authentication.",
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



class GetDishViews(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                decoded_payload = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})
                customer = Customer.objects.get(contact_number=decoded_payload['client_id'])
                
                meal_type = request.query_params.get('mealType')
                search_keyword = request.query_params.get('search')
                is_veg = request.query_params.get('isVeg')
                is_non_veg = request.query_params.get('isNonVeg')
                is_egg = request.query_params.get('isEgg')

                # Create a base queryset based on meal type
                if meal_type == "Breakfast":
                    base_queryset = Breakfast.objects.all()
                    serializer_class = BreakfastSerializer
                elif meal_type == "Lunch":
                    base_queryset = Lunch.objects.all()
                    serializer_class = LunchSerializer
                elif meal_type == "Dinner":
                    base_queryset = Dinner.objects.all()
                    serializer_class = DinnerSerializer
                elif meal_type == "Snacks":
                    base_queryset = Snacks.objects.all()
                    serializer_class = SnacksSerializer
                else:
                    response_data = {
                        "data": None,
                        "status": False,
                        "code": 400,
                        "message": "Invalid meal type provided.",
                    }
                    return Response(response_data)

                # Apply additional filters based on other query parameters
                # if is_veg:
                #     base_queryset = base_queryset.filter(is_veg=True)
                # if is_non_veg:
                #     base_queryset = base_queryset.filter(is_non_veg=True)
                # if is_egg:
                #     base_queryset = base_queryset.filter(is_egg=True)

                # Apply search filter
                if search_keyword:
                    base_queryset = base_queryset.filter(food__icontains=search_keyword)

                # Serialize the filtered queryset
                serializer = serializer_class(base_queryset, many=True)
                serializer_data_list = serializer.data
                response_data = []
                for data in serializer_data_list:
                    input_string = data['ingredients']
                    ingredients = input_string.split(",")  # Split the string into a list of ingredient
                    recipe_values = []
                    for ingredient in ingredients:
                        # Assuming you want to create a dictionary with a "name" key and a fixed "quantity" value
                        recipe_values.append({
                            "name": ingredient,
                        })
                    breakfast_item = {
                        "dishId": data['id'],
                        "dishName": data['food'],
                        "ingredients": data['ingredients'],
                        "calories": 400,
                        "nutritionValues": [
                          {
                            "name": data['oil'],
                            "quantity": data['quantity'],
                            "percentage":25,
                            "colour":"#01BA91",
                          }
                        ],
                        "recipeValues": recipe_values
                      }
                    response_data.append(breakfast_item)
                response_data = {
                    "data": response_data,
                        "status": True,
                        "code": 200
                    }
                return Response(response_data)

            except Exception as e:
                print(e)
                
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
            except Customer.DoesNotExist:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "Invalid Authentication.",
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
                
        else:
            response_data ={
                "data": None,
                "status": False,
                "code": 400,
                "message": "No token provided.",
            }
            return Response(response_data)



class AddCaloryViews(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        data = request.data
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                decoded_payload = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})
                try:
                    customer = Customer.objects.get(contact_number=decoded_payload['client_id'])
                    try:
                        calory = CaloryCount.objects.filter(customer=customer, dish=data["dish"], dish_type=data["dish_type"],date=data["date"]).first()
                    except CaloryCount.DoesNotExist:
                        calory = None
                    try:
                      print(request.data)
                      if all(key in data for key in ("dish_type", "dish", "calory", "action","date")):
                          if data["action"] == "add":
                              if calory is not None:
                                  # Update existing calory_data
                                  calory.calory += float(data["calory"])
                                  calory.save()
                              else:
                                  print("ufe")
                                  calory_data = CaloryCount(customer=customer, calory=data["calory"], dish=data["dish"], dish_type=data["dish_type"],date=data["date"])
                                  calory_data.save()
                  
                              calory_response = CaloryCount.objects.filter(customer=customer, date=data["date"])
                              serializer = CalorySerializer(calory_response, many=True)
                  
                              response_data = {
                                  "data": serializer.data,
                                  "status": True,
                                  "code": 200
                              }
                              return Response(response_data)
                          elif data["action"] == "remove":
                              if calory is not None and calory.calory > 0.0:
                                  print("dofep")
                                  # Update existing calory_data
                                  calory.calory -= float(data["calory"])
                                  calory.save()
                  
                              calory_response = CaloryCount.objects.filter(customer=customer, date=data["date"])
                              serializer = CalorySerializer(calory_response, many=True)
                  
                              response_data = {
                                  "data": serializer.data,
                                  "status": True,
                                  "code": 200
                              }
                              return Response(response_data)
                          else:
                              response_data = {
                                  "message": "Provide correct request data.",
                                  "status": True,
                                  "code": 400
                              }
                              return Response(response_data)
                      else:
                          response_data = {
                              "message": "Missing Required Field.",
                              "status": True,
                              "code": 400
                          }
                          return Response(response_data)

                    except Exception as e:
                      print(e)
                      response_data = {
                            "message": "An Error Occured.",
                            "status": True,
                            "code": 500                       
                        }
                      return Response(response_data)
                except Exception as e:
                    print(e)
                    response_data ={
                        "status": False,
                        "data": None,
                        "code": 401,
                        "message": "User Does't Exist.",
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
            except Customer.DoesNotExist:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "Invalid Authentication.",
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
                
        else:
            response_data ={
                "data": None,
                "status": False,
                "code": 400,
                "message": "No token provided.",
            }
            return Response(response_data)