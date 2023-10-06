from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .models import *
# from customer_engine.models_new_bkp import *
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
import math
# Create your views here.
from customer_engine.models import *
import csv
from django.http import HttpResponse

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST["password"]
        try:
            user = AdminUser.objects.get(email=email)
        except:
            user=None
        if user is not None and user.password == password:
            request.session["user"] = user.id
            request.session["password"] = user.password
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
        try:
            user = AdminUser.objects.get(email=email)
        except:
            user = None
        try:
            uploaded_image = request.POST["picture"]
            print(uploaded_image)
            if uploaded_image:
                print("hjsj")
                aws_access_key_id = 'AKIAU62W7KNUZ4DKGRU3'
                aws_secret_access_key = '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'
                aws_region = 'us-east-2'
                bucket_name = 'appstacklabs'
                s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
                object_key = f"admin/profile/images/{uploaded_image}"  # Adjust the path in the bucket as needed
                image_data = uploaded_image.read()
                # Upload the image data to S3 using put_object
                s3.put_object(Body=image_data, Bucket=bucket_name, Key=object_key)
                s3_image_url = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{object_key}"
            else:
                s3_image_url = "https://mdbootstrap.com/img/Photos/Others/placeholder-avatar.jpg"
        except Exception as e:
            print(e)
            s3_image_url = "https://mdbootstrap.com/img/Photos/Others/placeholder-avatar.jpg"
        print(s3_image_url)            
        if user:
            return render(request,"signup.html",{
                'tag':"danger",
                'message':"User already exist",
            })
        else:
            user_data = AdminUser(name=name,email=email,password=password,image_url = s3_image_url)
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
            print(otp)
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
    total_customer = Customer.objects.all().count()
    total_dishes = DailySnacks.objects.all().count()
    print(total_dishes,"---------------")
    return render(request,"index.html",{
        "user":user,
        "total_customer":total_customer,
        "total_dishes":total_dishes
    })


@custom_login_required
def add_customer(request):
    user = AdminUser.objects.get(id = request.session["user"])
    print(request.method ,"-------------------01")
    if request.method == "POST":
        print(request.POST,"=============02")
        
        firstname = request.POST["fname"]
        lastname = request.POST["lname"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        location = request.POST["city"] +" "+  request.POST["pincode"]
        contact = request.POST["mobile"]
        email = request.POST["email"]
        dob = request.POST["dob"]
        age = request.POST["age"]
        height = request.POST["height"]
        weight = request.POST["weight"]
        health_issue = request.POST["hissue"]
        other_issue = request.POST["oissue"]
        any_medication = request.POST["any-medication"]
        veg_nonveg = request.POST["veg-nonveg"]
        profession = request.POST["profession"]
        help = request.POST["help"]
        
        data = Customer(username = email, first_name = firstname, last_name = lastname ,gender = gender,address = address,
                        location = location, contact_number = contact, email = email, date_of_birth = dob, age = age ,
                        height = height, weight = weight, health_issue = health_issue, other_issue = other_issue, 
                        any_medication = any_medication, veg_nonveg = veg_nonveg, profession = profession , help=help)
        
        print(data,"==================")
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
    # filter_criteria = ['breakfast', 'lunch', 'dinner', 'evening_snacks'] 
    
    data = DailySnacks.objects.all()  
    return render(request,"recipe-management.html",{
        "user":user,
        "data": data
    })


@custom_login_required
def dish_calculator(request):
    user = AdminUser.objects.get(id = request.session["user"])
    print(user,"-----------")
    all_dishes = AddIngridient.objects.all()
    print(all_dishes,"********")
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
def recipe_calculator(request, id):
    user = AdminUser.objects.get(id = request.session["user"])
    data = AddRecipe.objects.get(id=id)
    ingridients = AddIngridient.objects.filter(item=data.id)
    print(data,"-------------")
    return render(request,"recipe-calculator-details.html",{
        "user":user,
        "recipe":data,
        "ingridients":ingridients
    })    

@custom_login_required
def customers_detail(request,user_id):
    user = AdminUser.objects.get(id = request.session["user"])
    data = UserSnacks.objects.get(customer = user_id)
    return render(request,"view-customer-detail.html",{
        "user":user,
        "data":data
    })
@custom_login_required
def view_more(request):
    user = AdminUser.objects.get(id = request.session["user"])
    return render(request,"view-more.html",{
        "user":user,
    })    
    
@custom_login_required
def customers_datatable(request):
    user = AdminUser.objects.get(id = request.session["user"])
    return render(request,"customers-datatable.html",{
        "user":user,
    })    

@custom_login_required
def add_dish(request):
    user = AdminUser.objects.get(id=request.session["user"])

    if request.method == "POST":
        file = request.FILES.get('uploaded-file')
        if file is not None and isinstance(file, InMemoryUploadedFile):
            try:
                xls = pd.ExcelFile(file)
                sheet_names = xls.sheet_names

                print(sheet_names)
                df = pd.read_excel(file, engine='openpyxl')
                print(data)
                for d in data:
                    for sheet in sheet_names:
                        dishes_data = None
                        if sheet == "Dishes":
                            dishes_data = AddIngridient(food=d["Food"], quantity=d["Quantity"],ingredients=d["Ingredients "],veg_nonveg_egg = d["Veg/Non Veg/Egg"],pral=d["PRAL"],gl=d["GL"], oil=d["Oil"],cals=d["Cals\nNet of  TDF"], aaf_adj_prot=d["AAF \nadj Prot"], carbs=d["Carbs          (Net of TDF)"], total_fat=d["Total Fat"], tdf=d["TDF"],sodium=d["Sodium"], potassium=d["Pota-ssium"], phasphorous=d["Phosphorus"], calcium=d["Calcium"], magnecium=d["Magnecium"], total_eaa=d["Total EAA"], lysine=d["Lysine"], gross_protine=d["Gross Protein"], free_suger=d["Free Sugars"],aa_factor=d["AA\nFactor"],glucose=d["GI       (Glu-cose)"])
                        elif sheet == "Breakfast":
                            dishes_data = Breakfast(food=d["Food"], quantity=d["Quantity"],ingredients=d["Ingredients "],veg_nonveg_egg = d["Veg/Non Veg/Egg"],pral=d["PRAL"],gl=d["GL"], oil=d["Oil"],cals=d["Cals\nNet of  TDF"], aaf_adj_prot=d["AAF \nadj Prot"], carbs=d["Carbs          (Net of TDF)"], total_fat=d["Total Fat"], tdf=d["TDF"],sodium=d["Sodium"], potassium=d["Pota-ssium"], phasphorous=d["Phosphorus"], calcium=d["Calcium"], magnecium=d["Magnecium"], total_eaa=d["Total EAA"], lysine=d["Lysine"], gross_protine=d["Gross Protein"], free_suger=d["Free Sugars"],aa_factor=d["AA\nFactor"],glucose=d["GI       (Glu-cose)"])
                        elif sheet == "Lunch":
                            dishes_data = Lunch(food=d["Food"], quantity=d["Quantity"],ingredients=d["Ingredients"],veg_nonveg_egg = d["Veg/Non Veg/Egg"],pral=d["PRAL"],gl=d["GL"], oil=d["Oil"],cals=d["Cals\nNet of  TDF"], aaf_adj_prot=d["AAF \nadj Prot"], carbs=d["Carbs          (Net of TDF)"], total_fat=d["Total Fat"], tdf=d["TDF"],sodium=d["Sodium"], potassium=d["Pota-ssium"], phasphorous=d["Phosphorus"], calcium=d["Calcium"], magnecium=d["Magnecium"], total_eaa=d["Total EAA"], lysine=d["Lysine"], gross_protine=d["Gross Protein"], free_suger=d["Free Sugars"])
                        elif sheet == "Dinner":
                            dishes_data = Diner(food=d["Food"], quantity=d["Quantity"],ingredients=d["Ingredients "],veg_nonveg_egg = d["Veg/Non Veg/Egg"],pral=d["PRAL"],gl=d["GL"], oil=d["Oil"],cals=d["Cals\nNet of  TDF"], aaf_adj_prot=d["AAF \nadj Prot"], carbs=d["Carbs          (Net of TDF)"], total_fat=d["Total Fat"], tdf=d["TDF"],sodium=d["Sodium"], potassium=d["Pota-ssium"], phasphorous=d["Phosphorus"], calcium=d["Calcium"], magnecium=d["Magnecium"], total_eaa=d["Total EAA"], lysine=d["Lysine"], gross_protine=d["Gross Protein"], free_suger=d["Free Sugars"],aa_factor=d["AA\nFactor"],glucose=d["GI       (Glu-cose)"])
                        elif sheet == "Breakfast":
                            dishes_data = Snacks(food=d["Food"], quantity=d["Quantity"],ingredients=d["Ingredients "],veg_nonveg_egg = d["Veg/Non Veg/Egg"],pral=d["PRAL"],gl=d["GL"], oil=d["Oil"],cals=d["Cals\nNet of  TDF"], aaf_adj_prot=d["AAF \nadj Prot"], carbs=d["Carbs          (Net of TDF)"], total_fat=d["Total Fat"], tdf=d["TDF"],sodium=d["Sodium"], potassium=d["Pota-ssium"], phasphorous=d["Phosphorus"], calcium=d["Calcium"], magnecium=d["Magnecium"], total_eaa=d["Total EAA"], lysine=d["Lysine"], gross_protine=d["Gross Protein"], free_suger=d["Free Sugars"],aa_factor=d["AA\nFactor"],glucose=d["GI       (Glu-cose)"])
                        if dishes_data is not None:
                            dishes_data.save()
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
            
            recipe_data = AddRecipe(item_name=item, sub_name=sub_item,quantity_type = quantity_type, quantity=quantity, quantity_help=quantity_help,type_of_meal=meal_type,type_of_food=food_type,health_condition=health_condition)
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
            
            recipe_data = AddRecipe(item_name=item, sub_name=sub_item,quantity_type = quantity_type, quantity=quantity, quantity_help=quantity_help,type_of_meal=meal_type,type_of_food=food_type,health_condition=health_condition)
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

# def recipe_details(request,recipe_id):
#     user = AdminUser.objects.get(id=request.session["user"])
#     recipe = AddRecipe.objects.get(id=recipe_id)
#     ingredients = AddIngridient.objects.filter(item=recipe)
#     return render(request,"recipe_details.html",{
#         "recipe":recipe,
#         "user":user,
#         "ingredients":ingredients
#     })

def recipe_details(request, recipe_id):
    print(recipe_id,'')
    user = AdminUser.objects.get(id = request.session["user"])
    data = DailySnacks.objects.get(id=recipe_id)
    
    return render(request,"recipe_details.html",{
        "user":user,
        "data":data
    })
    
# def add_ingredient(request):
#     user = AdminUser.objects.get(id = request.session["user"])
#     print("hi/hello")
#     print(user.image_url)
#     return render(request,"add-ingredient.html",{
#         "user":user
#     })

def add_ingredient(request):
    user = AdminUser.objects.get(id = request.session["user"])
    print(request.method ,"-------------------01")
    if request.method == "POST":
        print(request.POST,"=============02")
        ingridient_name = request.POST["ingridient_name"]
        quantity_type = request.POST["ingridient_type"]
        ingridient_quantity = request.POST["ingridient_quantity"]
        protein = request.POST["protein"]
        calories = request.POST["calories"]
        fat = request.POST["fat"]
        carbs = request.POST["carbs"]
        sugars = request.POST["sugars"]
        sodium = request.POST["sodium"]
        fiber = request.POST["fiber"]
        
        data = AddIngridient(
            ingridient_name=ingridient_name,
            quantity_type=quantity_type,
            ingridient_quantity=ingridient_quantity,
            protein=protein,
            calories=calories,
            fat=fat,
            carps=carbs,  
            sugars=sugars,
            sodium=sodium,
            fiber=fiber,
        )
        
        print(data,"==================")
        
        data.save()
        return render(request,"add_ingredient.html",{
            "user":user,
            "tag":"success",
            "message": "Ingridient Added Successfully."
        })
    return render(request,"add_ingredient.html",{
        "user":user,
    })

def ingredients_items(request):
    user = AdminUser.objects.get(id = request.session["user"])
    data = DailySnacks.objects.all()
    print(data,"*************")
    return render(request,"ingredients-items.html",{
        "user":user,
        "data":data
    })
    
@custom_login_required
def add_dish_calculator(request):
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
            
            ingridient_name = request.POST.getlist("ingridient-name")
            ingridient_qty_type = request.POST.getlist("ingridient-qty-type")
            ingridient_qty = request.POST.getlist("ingridient-qty")
            protein = request.POST.getlist("protein")
            calories = request.POST.getlist("calories")
            fat = request.POST.getlist("fat")
            carbs = request.POST.getlist("carbs")
            sugars = request.POST.getlist("sugars")
            sodium = request.POST.getlist("sodium")
            fiber = request.POST.getlist("fiber")
            
            dishes_data = AddRecipe(item_name=item, sub_name=sub_item,quantity_type = quantity_type, quantity=quantity, quantity_help=quantity_help,type_of_meal=meal_type,type_of_food=food_type)
            dishes_data.save()
            
            recipe = AddRecipe.objects.get(id=dishes_data.id)
            
            for i in range(len(ingridient_name)):
                ingridient = AddIngridient(
                    item=recipe,
                    ingridient_name=ingridient_name[i],
                    quantity_type=ingridient_qty_type[i] if ingridient_qty_type[i] else None,
                    ingridient_quantity=float(ingridient_qty[i]) if ingridient_qty[i] else None,
                    protein=float(protein[i]) if protein[i] else None,
                    calories=float(calories[i]) if calories[i] else None,
                    fat=float(fat[i]) if fat[i] else None,
                    carbs=float(carbs[i]) if carbs[i] else None,
                    sugars=float(sugars[i]) if sugars[i] else None,
                    sodium=float(sodium[i]) if sodium[i] else None,
                    fiber=float(fiber[i]) if fiber[i] else None
                )
                ingridient.save()
            
            messages.success(request, "Dishes Successfully Added.")
            return redirect("add_dish")
        except Exception as e:
            print(e)
            messages.success(request, "Something Wrong,Try Again.")
            return redirect("add_dish")
    return redirect("add_dish")
    
    
@custom_login_required
def upload_csv(request):
    # user = AdminUser.objects.get(id=request.session["user"])
    print(request.method ,"-------------------01")
    if request.method == 'POST':
        category = request.POST['category']
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            # Specify the encoding as 'latin-1' to handle extended character sets
            encoding = 'latin-1'

            try:
                # Attempt to read the CSV file using the specified encoding
                decoded_data = uploaded_file.read().decode(encoding)

                # Create a CSV DictReader
                reader = csv.DictReader(decoded_data.splitlines())

                # Create a list to store the processed data
                data = []

                # Process the CSV data as dictionaries (key-value pairs)
                for row in reader:
                    # You can access columns by their names as keys
                    print(row)

                    # Map CSV columns to model fields and append to the 'data' list
                    if len(row.get("Food", "")) > 0:
                        data.append({
                            'meal_type': category,  # Use the 'category' variable
                            'food': row.get('Food', ''),
                            'quantity': row.get('Quantity', ''),
                            'ingredients': row.get('Ingredients ', ''),
                            'veg_nonveg_egg': row.get('Veg/Non Veg/Egg', ''),
                            'pral': row.get('PRAL', ''),
                            'oil': row.get('Oil', ''),
                            'gl': row.get('GL', ''),
                            'cals': row.get('Cals\nNet of  TDF', ''),
                            'aaf_adj_prot': row.get('AAF \nadj Prot', ''),
                            'carbs': row.get('Carbs          (Net of TDF)', ''),
                            'total_fat': row.get('Total Fat', ''),
                            'tdf': row.get('TDF', ''),
                            'sodium': row.get('Sodium', ''),
                            'potassium': row.get('Pota-ssium', ''),
                            'phasphorous': row.get('Phosphorus', ''),
                            'calcium': row.get('Calcium', ''),
                            'magnecium': row.get('Magnecium', ''),
                            'total_eaa': row.get('Total EAA', ''),
                            'lysine': row.get('Lysine', ''),
                            'gross_protine': row.get('Gross Protein', ''),
                            'free_suger': row.get('Free Sugars', ''),
                            'aa_factor': 0,
                            'glucose': 0
                        })


                # Add your logic here to save or process the 'data' list as needed

                return HttpResponse("CSV file uploaded and processed successfully.")
            except UnicodeDecodeError as e:
                # Handle the encoding error, e.g., by returning an error message
                error_message = f"Error decoding file: {str(e)}"
                return HttpResponse(error_message, status=400)

    return render(request, "upload_csv.html")


def ingredients_items(request):
    user = AdminUser.objects.get(id = request.session["user"])
    data = DailySnacks.objects.all()
    print(data,"*************")
    return render(request,"ingredients-items.html",{
        "user":user,
        "data":data
})