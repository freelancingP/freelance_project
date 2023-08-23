from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .models import *
from customer_engine.models import *
from customer_engine.decorators import custom_login_required
from django.shortcuts import redirect
from django.urls import reverse
import random
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
from openpyxl import load_workbook
import boto3
# Create your views here.

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST["password"]
        print(email,password)
        try:
            user = AdminUser.objects.get(email=email)
        except:
            user=None
        if user is not None and user.password == password:
            request.session["user"] = user.id
            request.session["password"] = user.password
            print("vdfg9it")
            return redirect('dashboard')
        else:
            return render(request, "login.html", {
                'tag': "danger",
                'message': "Invalid credentials",
            })
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST['email']
        password = request.POST["password"]
        print(email,password)
        try:
            user = AdminUser.objects.get(email=email)
        except:
            user = None
        if user:
            return render(request,"signup.html",{
                'tag':"danger",
                'message':"User already exist",
            })
        else:
            user_data = AdminUser(name=name,email=email,password=password)
            user_data.save()
            print('cshuvev')
            return render(request,"signup.html",{
                'tag':"success",
                'message':"User Successfully Registered",
            })

    return render(request,"signup.html")

def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = AdminUser.objects.get(email=email)
        except:
            user = None
        if user:
            otp = random.randrange(100000, 999999)
            request.session["user"]= user.id
            request.session["otp"] = otp
            return redirect("verify_otp")
        else:
            return render(request,"reset_password.html",{
                'tag': 'danger', 
                'message': 'Email Id Not Found.'
            })
    return render(request,"reset_password.html")
        
def verify_otp(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        print(request.session["otp"])
        if int(otp) == request.session["otp"]:
            del request.session["otp"]
            return redirect("new_password")
        else:
            return render(request,"verify_otp.html",{
                'tag': 'danger', 
                'message': 'Invalid OTP'
            })
    return render(request,"verify_otp.html")

def logout(request):
    if "user" in request.session:
        del request.session["user"]
        return redirect("login")
    else:
        return render(request, "login.html",{
            'message': "User was not logged In",
        })


def new_password(request):
    if request.method == "POST":
        try:
            user = AdminUser.objects.get(id = request.session["user"])
        except:
            user = None
        new_password = request.POST["new-pass"]
        confirm_password = request.POST["confirm-pass"]
        if user:
            if new_password == confirm_password:
                user.password = new_password
                user.save()
                del request.session["user"]
                return render(request,"new_password.html",{
                    "message":"Your password successfully changed.",
                    "user":user
                })
            else:
                return render(request,"new_password.html",{
                    "message":"Password did't matched,Try again!",
                    "user":user
                })
        else:
            messages.success(request,"Something Wrong, Try again.")
            return redirect("reset_password")

        
    return render(request,"new_password.html")

@custom_login_required
def index(request):
    user = AdminUser.objects.get(id = request.session["user"])
    print(user)
    return render(request,"index.html",{
        "user":user
    })

@custom_login_required
def add_customer(request):
    user = AdminUser.objects.get(id = request.session["user"])
    if request.method == "POST":
        print(request.POST)
        # customer_type = request.POST["customer_type"]
        firstname = request.POST["fname"]
        lastname = request.POST["lname"]
        gender = request.POST["gender"]
        location = request.POST["location"]
        address = request.POST["address"]
        contact = request.POST["mobile"]
        email = request.POST["email"]
        dob = request.POST["dob"]
        age = request.POST["age"]
        height = request.POST["height"]
        weight = request.POST["weight"]
        height_unit = request.POST["height_unit"]
        weight_unit = request.POST["weight_unit"]
        health_issue = request.POST["hissue"]
        other_issue = request.POST["oissue"]
        any_medication = request.POST["any-medication"]
        veg_nonveg = request.POST["veg-nonveg"]
        profession = request.POST["profession"]
        help = request.POST["help"]
        try:
            uploaded_image = request.POST["picture"]
            aws_access_key_id = 'AKIAU62W7KNUZ4DKGRU3'
            aws_secret_access_key = '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'
            aws_region = 'us-east-2'
            bucket_name = 'appstacklabs'
            s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
            object_key = f"images/{uploaded_image}"  # Adjust the path in the bucket as needed
            image_data = uploaded_image
            # Upload the image data to S3 using put_object
            s3.put_object(Body=image_data, Bucket=bucket_name, Key=object_key)
            s3_image_url = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{object_key}"
        except Exception as e:
            s3_image_url = None
        data = Customer(image_url = s3_image_url, first_name = firstname, last_name = lastname ,gender = gender,location = location, address = address, contact_number = contact,email = email, date_of_birth = dob, age = age , height = height,height_unit=height_unit, weight = weight,weight_unit=weight_unit, health_issue = health_issue, other_issue = other_issue, any_medication = any_medication, veg_nonveg = veg_nonveg, profession = profession , help=help)
        print(data)
        customer_exists = Customer.objects.filter(Q(contact_number=contact) | Q(email=email)).exists()
        if customer_exists:
            return render(request,"add_customer.html",{
                "user":user,
                "tag":"danger",
                "message": "Email or Phone Number already exists."
            })
        else:
            data.save()
            return render(request,"add_customer.html",{
                "user":user,
                "tag":"success",
                "message": "Customer Added Successfully."
            })
    return render(request,"add_customer.html",{
        "user":user,
    })

@custom_login_required
def customers(request):
    user = AdminUser.objects.get(id = request.session["user"])
    data = Customer.objects.all()
    return render(request,"customers-datatable.html",{
        "user":user,
        "data":data
    })

@custom_login_required
def recipe_management(request):
    user = AdminUser.objects.get(id = request.session["user"])
    return render(request,"recipe-management.html",{
        "user":user
    })

@custom_login_required
def dish_calculator(request):
    user = AdminUser.objects.get(id = request.session["user"])
    all_dishes = Dishes.objects.all()
    return render(request,"dish-calculator-items.html",{
        "user":user,
        "dishes":all_dishes
    })

@custom_login_required
def recipe_list(request):
    user = AdminUser.objects.get(id = request.session["user"])
    all_recipe = AddRecipe.objects.all()
    return render(request,"recipe.html",{
        "user":user,
        "all_recipe":all_recipe
    })

@custom_login_required
def customers_detail(request,user_id):
    user = AdminUser.objects.get(id = request.session["user"])
    customer = Customer.objects.get(id= user_id)
    return render(request,"view-customer-detail.html",{
        "user":user,
        "customer":customer
    })

@custom_login_required
def add_dish(request):
    user = AdminUser.objects.get(id=request.session["user"])

    if request.method == "POST":
        file = request.FILES.get('uploaded-file')
        if file is not None and isinstance(file, InMemoryUploadedFile):
            try:
                df = pd.read_excel(file, engine='openpyxl')  # Explicitly specify the engine
                data = df.to_dict(orient='records')
                for d in data:
                    # Your code to save data to the database goes here
                    dishes_data = Dishes(food=d["Food"], quantity=d["Quantity (gms)"], pral=d["PRAL"], oil=d["Oil"], glycemicload=d["Glycemic load"], calories=d["Calories\n"], aaf_adj_prot=d["AAF \nadj Prot"], carbohydtrates=d["Carbohydrates        "], total_fat=d["Total Fat"], tdf=d["TDF"], sodium=d["Sodium"], potassium=d["Pota-ssium"], phasphorous=d["Phosphorus"], calcium=d["Calcium"], magnecium=d["Magnecium"], total_eaa=d["Total EAA"], lysine=d["Lysine"], gross_protine=d["Gross Protein"], free_suger=d["Free Sugars"])
                    dishes_data.save()
                print(data)
                return render(request, "add-dish-calculator.html", {
                    "user": user,
                    "tag": "success",
                    "message": "Dishes Successfully Added in Database."
                })
            except Exception as e:
                return render(request, "add-dish-calculator.html", {
                    "user": user,
                    "tag": "danger",
                    "message": f"Error while processing the Excel file: {str(e)}"
                })
        else:
            return render(request, "add-dish-calculator.html", {
                "user": user,
                "tag": "danger",
                "message": "No file uploaded or invalid file format."
            })
    return render(request, "add-dish-calculator.html", {
        "user": user
    })

@custom_login_required
def add_recipe(request):
    if request.method == "POST":
        try:
            print(request.POST)
            item = request.POST["item-name"]
            sub_item = request.POST["sub-name"]
            quantity_type = request.POST["qty-type"]
            quantity = request.POST["qty"]
            quantity_help = request.POST.get("qty-help")
            meal_type = request.POST["meal-type"]
            food_type = request.POST["food-type"]
            health_condition = request.POST["health-condition"]
            if not quantity_help:
                quantity_help = None
            
            ingridient_name = request.POST.getlist("ingridient-name")
            ingridient_qty_type = request.POST.getlist("ingridient-qty-type")
            ingridient_qty = request.POST.getlist("ingridient-qty")
            protein = request.POST.getlist("protein")
            calories = request.POST.getlist("calories")
            fat = request.POST.getlist("fat")
            carps = request.POST.getlist("carps")
            sugars = request.POST.getlist("sugars")
            sodium = request.POST.getlist("sodium")
            fiber = request.POST.getlist("fiber")
            
            recipe_data = AddRecipe(item_name=item, sub_name=sub_item, quantity=quantity, quantity_help=quantity_help,type_of_meal=meal_type,type_of_food=food_type,health_condition=health_condition)
            recipe_data.save()
            recipe = AddRecipe.objects.get(id=recipe_data.id)
            
            for i in range(len(ingridient_name)):
                ingridient = AddIngridient(
                    item=recipe,
                    ingridient_name=ingridient_name[i],
                    quantity_type=ingridient_qty_type[i] if ingridient_qty_type[i] else None,
                    ingridient_quantity=float(ingridient_qty[i]) if ingridient_qty[i] else None,
                    protein=float(protein[i]) if protein[i] else None,
                    calories=float(calories[i]) if calories[i] else None,
                    fat=float(fat[i]) if fat[i] else None,
                    carps=float(carps[i]) if carps[i] else None,
                    sugars=float(sugars[i]) if sugars[i] else None,
                    sodium=float(sodium[i]) if sodium[i] else None,
                    fiber=float(fiber[i]) if fiber[i] else None
                )
                ingridient.save()
            
            messages.success(request, "Recipe Successfully Added.")
            return redirect("add_dish")
        except Exception as e:
            print(e)
            messages.success(request, "Something Wrong,Try Again.")
            return redirect("add_dish")
    return redirect("add_dish")


def recipe_details(request,recipe_id):
    user = AdminUser.objects.get(id=request.session["user"])
    recipe = AddRecipe.objects.get(id=recipe_id)
    ingredients = AddIngridient.objects.filter(item=recipe)
    return render(request,"recipe_details.html",{
        "recipe":recipe,
        "user":user,
        "ingredients":ingredients
    })