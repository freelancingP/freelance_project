import csv
import json
from customer_engine.models import Dishes

def import_json_data_from_file(json_file_path):
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        for item in json_data:
            Dishes.objects.create(**item)

# Usage
json_file_path = ['breakfast.json','lunch.json','dinner.json','evening_snacks.json']
for file_path in json_file_path:
    import_json_data_from_file(file_path)






# def convert_csv_to_json(csv_file_path, meal_type):
#     data = []
#     with open(csv_file_path, mode='r') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for row in csv_reader:
#             print(row,'--')
#             if len(row["Food"]) > 0:
#                 # Map CSV columns to model fields
#                 data.append({
#                     'meal_type':meal_type,
#                     'food': row['Food'],
#                     'quantity': row['Quantity'],
#                     'ingredients': row['Ingredients '],
#                     'veg_nonveg_egg': row['Veg/Non Veg/Egg'],
#                     'pral': row['PRAL'],
#                     'oil': row['Oil'],
#                     'gl': row['GL'],
#                     'cals': row['Cals\nNet of  TDF'],
#                     'aaf_adj_prot': row['AAF \nadj Prot'],
#                     'carbs': row['Carbs          (Net of TDF)'],
#                     'total_fat': row['Total Fat'],
#                     'tdf': row['TDF'],
#                     'sodium': row['Sodium'],
#                     'potassium': row['Pota-ssium'],
#                     'phasphorous': row['Phosphorus'],
#                     'calcium': row['Calcium'],
#                     'magnecium': row['Magnecium'],
#                     'total_eaa': row['Total EAA'],
#                     'lysine': row['Lysine'],
#                     'gross_protine': row['Gross Protein'],
#                     'free_suger': row['Free Sugars'],
#                     'aa_factor':0,
#                     'glucose':0
#                 })
#     return data

# # Usage
# csv_file_path = '/Users/root1/Documents/work/Appstack/data/breakfast.csv'
# json_data = convert_csv_to_json(csv_file_path, 'breakfast')
# # Save as JSON file
# with open('breakfast.json', 'w') as json_file:
#     json.dump(json_data, json_file)



# # Usage
# csv_file_path = '/Users/root1/Documents/work/Appstack/data/lunch.csv'
# json_data = convert_csv_to_json(csv_file_path, 'lunch')
# # Save as JSON file
# with open('lunch.json', 'w') as json_file:
#     json.dump(json_data, json_file)




# # Usage
# csv_file_path = '/Users/root1/Documents/work/Appstack/data/dinner.csv'
# json_data = convert_csv_to_json(csv_file_path, 'dinner')
# # Save as JSON file
# with open('dinner.json', 'w') as json_file:
#     json.dump(json_data, json_file)




# # Usage
# csv_file_path = '/Users/root1/Documents/work/Appstack/data/evening_snacks.csv'
# json_data = convert_csv_to_json(csv_file_path, 'evening_snacks')
# # Save as JSON file
# with open('evening_snacks.json', 'w') as json_file:
#     json.dump(json_data, json_file)




# def import_json_data_from_file(json_file_path):
#     with open(json_file_path, 'r') as json_file:
#         json_data = json.load(json_file)
#         for item in json_data:
#             DailySnacks.objects.create(**item)

# # Usage
# json_file_path = 'evening_snacks.json'
# import_json_data_from_file(json_file_path)



# 

import csv
from customer_engine.models import Dishes

def import_csv_data(csv_file_path):
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            print(row,'--')
            oil_value = row['Oil']

            if len(row["Food"]) > 0:
                # Map CSV columns to model fields
                data = {
                    # 'type':type,
                    'food': row['Food'],
                    'price': row['Price'],
                    'oil': oil_value,
                    'gl': row['GL'],
                    'useble_cals': row['Useble Cals'],
                    'aaf_adj_prot': row['AAF \nadj\n Prot'],
                    'carbs': row['CarbsNet of\nTDF'],
                    'total_fat': row['Total Fat'],
                    'tdf': row['TDF'],
                    'sodium': row['Sodium'],
                    'potassium': row['Potassium'],
                    'phasphorous': row['Phosphorus'],
                    'calcium': row['Calcium'],
                    'magnecium': row['Magnecium'],
                    'total_eaa': row['Total EAA'],
                    'lysine': row['Lysine'],
                    'gross_protine': row['Gross Prot-ein'],
                    'free_suger': row['Free Sugar'],
            
                }
                Dishes.objects.create(**data)



csv_file_path = 'Ingredients List (3).csv'
import_csv_data(csv_file_path)

# csv_file_path = '/home/sh-root/Documents/Appstack/freelance_project/Ingredients List (3)/dals.csv'
# import_csv_data(csv_file_path,"dals")

# csv_file_path = '/home/sh-root/Documents/Appstack/freelance_project/Ingredients List (3)/fruits.csv'
# import_csv_data(csv_file_path, 'fruits')

# csv_file_path = '/home/sh-root/Documents/Appstack/freelance_project/Ingredients List (3)/helth_drinks.csv'
# import_csv_data(csv_file_path, 'helth_drinks')

# csv_file_path = '/home/sh-root/Documents/Appstack/freelance_project/Ingredients List (3)/milk_product.csv'
# import_csv_data(csv_file_path, 'milk_product')

# csv_file_path = '/home/sh-root/Documents/Appstack/freelance_project/Ingredients List (3)/non_veg.csv'
# import_csv_data(csv_file_path, 'non_veg')

# csv_file_path = '/Users/root1/Documents/work/Appstack/data/nuts_&_oil_seeds.csv'
# import_csv_data(csv_file_path, 'nuts_&_oil_seeds')

# csv_file_path = '/Users/root1/Documents/work/Appstack/data/spices.csv'
# import_csv_data(csv_file_path, 'spices')

# csv_file_path = '/Users/root1/Documents/work/Appstack/data/veges_greens.csv'
# import_csv_data(csv_file_path, 'veges_greens')

# csv_file_path = '/Users/root1/Documents/work/Appstack/data/veges_root_&_tubers.csv'
# import_csv_data(csv_file_path, 'veges_root_&_tubers')

# csv_file_path = '/Users/root1/Documents/work/Appstack/data/veges_others.csv'
# import_csv_data(csv_file_path, 'veges_others')

# csv_file_path = '/Users/root1/Documents/work/Appstack/data/veggies_fit_for_life.csv'
# import_csv_data(csv_file_path, 'veggies_fit_for_life')