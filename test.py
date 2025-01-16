import requests
import pandas as pd
import json
import math
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['car_db']
collection = db['getaround_cars_data']

# API endpoint
url = "https://getaround.com/search.json"

cities = [
    {"name": "Paris", "lat": "48.8566", "lon": "2.3522"},
    {"name": "Marseille", "lat": "43.2965", "lon": "5.3698"},
    {"name": "Lyon", "lat": "45.7640", "lon": "4.8357"},
    {"name": "Toulouse", "lat": "43.6047", "lon": "1.4442"},
    {"name": "Nice", "lat": "43.7102", "lon": "7.2620"},
    {"name": "Nantes", "lat": "47.2184", "lon": "-1.5536"},
    {"name": "Montpellier", "lat": "43.6108", "lon": "3.8767"},
    {"name": "Strasbourg", "lat": "48.5734", "lon": "7.7521"},
    {"name": "Bordeaux", "lat": "44.8378", "lon": "-0.5792"},
    {"name": "Lille", "lat": "50.6292", "lon": "3.0573"},
    {"name": "Rennes", "lat": "48.1173", "lon": "-1.6778"},
    {"name": "Grenoble", "lat": "45.1885", "lon": "5.7245"},
    {"name": "Dijon", "lat": "47.3220", "lon": "5.0415"},
    {"name": "Le Havre", "lat": "49.4944", "lon": "0.1079"}
]

all_cars = []
unique_cars = {}

for city in cities:
    param_set = {
        "address": city["name"],
        "latitude": city["lat"],
        "longitude": city["lon"],
        "country_scope": "FR",
        "start_date": "2025-01-30",
        "start_time": "07:00",
        "end_date": "2025-01-31",
        "end_time": "07:30",
        "display_view": "list",
        "pickup_method": "",
        "program": "getaround",
        "view_mode": "list",
        "picked_cars_attributes": "EMPTY"
    }
    page = 1
    while True:
        param_set['page'] = page
        response = requests.get(url, params=param_set)
        
        if response.status_code == 200:
            data = response.json()
            if 'cars' in data:
                for car in data['cars']:
                    car_id = car.get('id')
                    if car_id not in unique_cars:
                        unique_cars[car_id] = car
                if 'total_count' in data:
                    total_count = data['total_count']
                    total_pages = math.ceil(total_count / 40)
                    if page >= total_pages:
                        break
                    page += 1
                else:
                    break
            else:
                print(f"No 'cars' key found in the data for {param_set['address']}")
                break
            print("/")
        else:
            print(f"Error for {param_set['address']}: {response.status_code}")
            print(response.text)
            break
    print("completed about ", city["name"])

all_cars = list(unique_cars.values())

if all_cars:
    # Save to CSV
    df = pd.DataFrame(all_cars)
    df.to_csv('getaround_data.csv', index=False)
    print("Data successfully saved to getaround_data.csv")
    
    # Save to MongoDB
    collection.insert_many(all_cars)
    print("Data successfully saved to MongoDB")
else:
    print("No car data found for any location")

# Close MongoDB connection
client.close()
