import requests
import pandas as pd

url = "https://arval-prod-euw-appservice-portalapi.azurewebsites.net/api/Announcements/5"

def fetch_data(page_number):
    params = {
        "orderBy": "createdAt|desc",
        "pageNumber": page_number,
        "pageSize": 20,
        "purchaseOption": "release",
        "reservationLabels": "available",
        "utm_source": "Mini-site Retail Part"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data for page {page_number}. Status code: {response.status_code}")
        return None

all_announcements = []
current_page = 1

while True:
    data = fetch_data(current_page)
    if data is None:
        break

    announcements = data.get('announcements', [])
    all_page_quantity = announcements.get('allPageQuantity', 0)
    announcements = announcements.get('announcements', [])
    all_announcements.extend(announcements)

    if current_page >= all_page_quantity:
        break

    current_page += 1
    print(f"Fetched page {current_page - 1} of {all_page_quantity}")

if all_announcements:
    df = pd.DataFrame(all_announcements)
    df.to_csv('announcements.csv', index=False)
    print(f"Data has been successfully saved to announcements.csv")
    print(f"Total announcements fetched: {len(all_announcements)}")
else:
    print("No data was fetched.")
