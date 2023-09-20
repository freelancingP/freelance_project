import csv
import json
from customer_engine.models import DailySnacks

def import_json_data_from_file(json_file_path):
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        for item in json_data:
            DailySnacks.objects.create(**item)
            
# Usage
json_file_path = ['breakfast.json', 'lunch.json', 'dinner.json', 'evening_snacks.json']
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







# # 
# def import_csv_data(csv_file_path, meal_type):
#     with open(csv_file_path, mode='r') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for row in csv_reader:
#             print(row,'--')
#             if len(row["Food"]) > 0:
#                 # Map CSV columns to model fields
#                 data = {
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
#                 }
#                 DailySnacks.objects.create(**data)



# csv_file_path = '/Users/root1/Documents/work/Appstack/data/breakfast.csv'
# import_csv_data(csv_file_path, 'breakfast')


# csv_file_path = '/Users/root1/Documents/work/Appstack/data/lunch.csv'
# import_csv_data(csv_file_path, 'lunch')


# csv_file_path = '/Users/root1/Documents/work/Appstack/data/dinner.csv'
# import_csv_data(csv_file_path, 'dinner')

# csv_file_path = '/Users/root1/Documents/work/Appstack/data/evening_snacks.csv'
# import_csv_data(csv_file_path, 'evening_snacks')