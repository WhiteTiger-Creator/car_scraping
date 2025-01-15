import requests
import csv

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

def write_to_csv(cars, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = cars[0].keys() if cars else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        for car in cars:
            writer.writerow(car)

def main():
    page = 1
    all_cars = []
    
    while True:
        car_data = fetch_car_data(page)
        if not car_data or 'groups' not in car_data:
            break
        
        cars = car_data['groups']
        all_cars.extend(cars)
        write_to_csv(cars, 'car_data.csv')
        print("car length", len(cars))
        
        if len(cars) < 24:
            break
        
        page += 1

    print(f"Total cars fetched: {len(all_cars)}")
    print("Car data has been successfully written to car_data.csv")

if __name__ == "__main__":
    main()
