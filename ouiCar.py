import requests
from pymongo import MongoClient
import json

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Adjust this if your MongoDB is not on localhost
db = client['car_db']  # Create or use a database named 'turo_database'
collection = db['ouicar_car_data']  # Create or use a collection named 'car_listings'

# Request URL
url = "https://turo.com/api/v2/search"

# Payload (request body)
payload = {
    "filters": {
        "location": {
            "country": "FR",
            "type": "area",
            "point": {
                "lat": "46.2276380",
                "lng": "2.2137490"
            }
        },
        "engines": [],
        "features": [],
        "makes": [],
        "models": [],
        "tmvTiers": [],
        "types": []
    },
    "dates": {
        "start": "2025-01-17T10:00",
        "end": "2025-01-20T10:00"
    },
    "sorts": {
        "direction": "ASC",
        "type": "RELEVANCE"
    }
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Origin": "https://turo.com",
    "Referer": "https://turo.com/us/en/search?country=FR&defaultZoomLevel=11&deliveryLocationType=city&endDate=01%2F20%2F2025&endTime=10%3A00&isMapSearch=false&itemsPerPage=200&latitude=46.227638&location=France&locationType=CITY&longitude=2.213749&pickupType=ALL&placeId=ChIJMVd4MymgVA0R99lHx5Y__Ws&sortType=RELEVANCE&startDate=01%2F17%2F2025&startTime=10%3A00&useDefaultMaximumDistance=true",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "traceparent": "00-c0e7287bea4e941cf3da1ad64cb7c36e-61de41a3be98f67b-01",
    "tracestate": "721478@nr=0-1-3069551-1022796076-61de41a3be98f67b----1736947667939"
}

# Cookies
cookies = {
    "_cfuvid": "bEqZ5q6lZRMonGe7ivtMdExC..ZxIxhqDD1Ik1.51gw-1736747019853-0.0.1.1-604800000",
    "rr_u_cid": "kMo3kgs7SfGglE9xIz12sA",
    "osano_consentmanager_uuid": "6a130d3c-6906-433a-8ed4-ebfad6f58635",
    "osano_consentmanager": "z-RkuJm7A_EEM4kkjqpMwEyU4Kyq-K7ZWrX7EqJsPMNQ8zf68NjFbU4Apl8YCrvoMzely-4o5Ls9aQEl6hmGtBtOcbKsSL8nb_a6tHTUmC_zOxTnGDJzK_gT5XHX7jNROWzbNJfy6XumimdHMHWjYr0sJ-gdjinYdOI2jdbglkEFTVMOsJgBuL_jGNNlu7owCeJMjPHq-r3-o8FtBN5Em_W0NGqwg8gUgIgGIhkkoktlrE5VhOsqrggbe-sxf11mtDs6a6ooso7JsCDqBvV956TkhDfswVEioIMYmWrfsUPBixpY8BSC28c02jz2oeUKGQMVZiOSGnQ",
    "sid": "yaSUsAI_Qvu9_HnBdmfyIg",
    "preferredLocale": "en-US",
    "__cf_bm": "rBkbLGcUbiQ3MddnIEy8IckLkQUUpSJcTtCFxmThreM-1736947561-1.0.1.1-uuswn9KUMaq08b.6r0PvX30vvydNlx6K42a50NOs8ajkv2jyrnfB6URuUGWBWtJn8k_ex6k3Ay63CLOJE2DOL.5g_8UmI.o3Qy61z0u9Ucg",
}

# Send the POST request
response = requests.post(url, json=payload, headers=headers, cookies=cookies)

# Handling the response
if response.status_code == 200:
    print("Request succeeded!")
    data = response.json()  # Parse JSON response
    
    # Save to MongoDB
    result = collection.insert_one(data)
    print(f"Data saved to MongoDB with id: {result.inserted_id}")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)  # Print raw response for debugging

# Close the MongoDB connection
client.close()
