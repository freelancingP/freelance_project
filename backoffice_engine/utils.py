from datetime import datetime
from  customer_engine.models import DailySnacks, UserSnacks
from django.db.models import Sum

def get_customer_data(date, customer, meal_type=None):

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
    
    column_names = [
            'id','meal_type', 'ingredients', 'food', 'cals', 'sodium', 'pral', 'oil', 'gl', 'aaf_adj_prot', 'carbs', 'total_fat', 'tdf',
            'potassium', 'phosphorus', 'calcium', 'magnesium', 'total_eaa', 'lysine',
            'gross_protein', 'free_sugar', 'aa_factor', 'glucose',
        ]

    date_obj = datetime.strptime(date, "%Y-%m-%d").date()  

    dish_ids_list = UserSnacks.objects.filter(customer=customer.id, updated_at__date=date_obj).values_list('dish_id', flat=True)

    data_queryset = None
    if meal_type:
        data_queryset = DailySnacks.objects.filter(id__in=dish_ids_list, meal_type=meal_type).values(*column_names)
    else:
        data_queryset = DailySnacks.objects.filter(id__in=dish_ids_list).values(*column_names)

    data = (
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
    data['total_calory'] = total_calory
    
    food_data = []
    unique_ingredients = set()

    for item in data_queryset:
       food_data.append(item)

    data['items'] = food_data

    # calories_used = 0
    # total_carbs = 0
    # total_calcium = 0

    # data = {
    #     'calories_used':0,
    #     'total_calory':total_calory,
    #     'calorie_breakdown':None,
    #     'breakfast':[],
    #     'lunch':[],
    #     'dinner':[],
    #     'evening_snacks':[],
    #     'added_dish':dish_ids_list
    # }

    # for instance in daily_snacks:
    #     data[instance.meal_type].append({
    #                 "id": instance.id,
    #                 "food": instance.food,
    #                 "ingredients": instance.ingredients,
    #                 "cals": instance.cals,
    #             })
    #     if instance.cals:
    #         calories_used += instance.cals

    #     if instance.carbs:
    #         total_carbs += instance.carbs

    #     if instance.calcium:
    #         total_calcium += instance.calcium


    # update data
    # calorie_breakdown = {
    #     "calories": {
    #             'value':calories_used,
    #             'color':'#2CA3FA',
    #             'percentage': 1                
    #         },
    #     "carbs": {
    #             'value':total_carbs,
    #             'color':'#FF7326',
    #             'percentage': 2
    #         },
    #     "calcium": {
    #             'value':total_calcium,
    #             'color':'#81BE00',
    #             'percentage': 3
    #         }
    # }

    # data['calorie_breakdown'] = calorie_breakdown
    # data['calories_used'] = calories_used
    # data['total_calory'] = total_calory
    print(data,'-------abcde')
    return data