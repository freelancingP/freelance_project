from datetime import datetime
from  customer_engine.models import DailySnacks, UserSnacks

def get_customer_data(date, customer):

    total_calory = 0

    try:
        if customer.gender == "Male":
            calory = 88.362+(float(customer.weight)*13.37)+(float(customer.height)*4.799)-(float(customer.age)*5.677)
            total_calory = round((calory * 0.702050619834711),2)
        elif customer.gender == "Female":
            calory = 447.593+(float(customer.weight)*9.247)+(float(customer.height)*3.098)-(float(customer.age)*4.33)
            total_calory = round((calory * 0.702050619834711),2)
    except:
        pass
    
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()  

    dish_ids_list = UserSnacks.objects.filter(customer=customer.id, updated_at__date=date_obj).values_list('dish_id', flat=True)

    daily_snacks = DailySnacks.objects.filter(id__in=dish_ids_list)

    calories_used = 0
    total_carbs = 0
    total_calcium = 0

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
            calories_used += instance.cals

        if instance.carbs:
            total_carbs += instance.carbs

        if instance.calcium:
            total_calcium += instance.calcium

    # update data
    calorie_breakdown = {
        "calories": {
                'value':calories_used,
                'color':'#2CA3FA',
                'percentage': 1                
            },
        "carbs": {
                'value':total_carbs,
                'color':'#FF7326',
                'percentage': 2
            },
        "calcium": {
                'value':total_calcium,
                'color':'#81BE00',
                'percentage': 3
            }
    }

    data['calorie_breakdown'] = calorie_breakdown
    data['calories_used'] = calories_used
    data['total_calory'] = total_calory

    return data