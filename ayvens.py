import requests
from pymongo import MongoClient

def fetch_car_data(page):
    url = "https://www.ayvens.com/api2/cars/queries/groups/"
    params = {
        "limit": 24,
        "page": page
    }
    headers = {
        "x-lpd-countrycode": "FR",
        "x-lpd-locale": "fr-FR"
    }
    response = requests.put(url, params=params, headers=headers)
    return response.json() if response.status_code == 200 else None

def save_to_mongodb(cars, db_name, collection_name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    collection = db[collection_name]
    if cars:
        collection.insert_many(cars)

def main():
    page = 1
    all_cars = []
    
    while True:
        car_data = fetch_car_data(page)
        if not car_data or 'groups' not in car_data:
            break
        
        cars = car_data['groups']
        all_cars.extend(cars)
        save_to_mongodb(cars, 'car_db', 'ayvens_car_data')
        print("Cars saved:", len(cars))
        
        if len(cars) < 24:
            break
        
        page += 1

    print(f"Total cars fetched and saved: {len(all_cars)}")
    print("Car data has been successfully saved to MongoDB")

if __name__ == "__main__":
    main()
