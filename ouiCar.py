import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Automatically download and install chromedriver if not available
chromedriver_autoinstaller.install()

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (useful in some environments)
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Set up the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to Turo search page with specified parameters
url = "https://turo.com/us/en/search?country=FR&defaultZoomLevel=11&delivery=false&deliveryLocationType=city&endDate=2025-02-14&isMapSearch=false&itemsPerPage=200&latitude=48.8566969&longitude=2.3514616&pickupType=ALL&placeId=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&sortType=RELEVANCE&startDate=2025-01-14&useDefaultMaximumDistance=true"
driver.get(url)

# Wait for the car listings to load
wait = WebDriverWait(driver, 20)  # Increase wait time to 20 seconds

try:
    # Wait for car elements to be visible
    car_elements = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".searchResult")))
except Exception as e:
    print(f"Error while waiting for elements: {e}")
    print("Page source at error:")
    print(driver.page_source)  # Print the page source for debugging
    driver.quit()
    exit()

# Extract car data
cars_data = []
for car in car_elements:
    try:
        make_model = car.find_element(By.CSS_SELECTOR, ".vehicleCardHeader h3").text
        price = car.find_element(By.CSS_SELECTOR, ".price").text
        cars_data.append({"Make and Model": make_model, "Price": price})
    except Exception as e:
        print(f"Error extracting data from a car element: {e}")
        continue

# Close the browser after data extraction
driver.quit()

# Create a DataFrame and save to CSV
if cars_data:
    df = pd.DataFrame(cars_data)
    df.to_csv('turo_car_rentals.csv', index=False)
    print("Data successfully saved to turo_car_rentals.csv")
else:
    print("No car data found.")
