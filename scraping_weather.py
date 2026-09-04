# Scraping weather data from timeanddate.com using Selenium with Edge WebDriver
# This script scrapes historical weather data for 2025 year for two locations: Novosibirsk and Raleigh.

# Note. We decided to use Edge WebDriver because it works stable comparing to Chrome. 
import csv
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Options for Edge
options = webdriver.EdgeOptions()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

# Define the cities and their corresponding URLs for scraping
CITIES = [
    {"city": "Novosibirsk", "url": "https://www.timeanddate.com/weather/russia/novosibirsk/historic"},
    {"city": "Raleigh", "url": "https://www.timeanddate.com/weather/usa/raleigh/historic"}
]

all_records = []

try:
    for location in CITIES:
        city_name = location["city"]
        print(f"\n--- Scraping {city_name} ---")

        # Loop through each month of the year 2025
        for month in range(1, 13):
            url = f"{location['url']}?month={month}&year=2025"
            print(f"Loading: {url}")
            
            driver.get(url)
            time.sleep(3)

            # Find the table containing the weather data
            table = driver.find_element(By.CSS_SELECTOR, "table")
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

            for row in rows:
                th = row.find_elements(By.TAG_NAME, "th")
                tds = row.find_elements(By.TAG_NAME, "td")

                if th and tds:
                    # Extract the metric name: High / Low / Avg 
                    metric = th[0].text.strip()
                    if "Reported" in metric or not metric:
                        continue

                    all_records.append({
                        "city": city_name,
                        "month": month,
                        "metric": metric,
                        "temperature": tds[0].text.strip() if len(tds) > 0 else "",
                        "humidity": tds[1].text.strip() if len(tds) > 1 else "",
                        "pressure": tds[2].text.strip() if len(tds) > 2 else ""
                    })

    print("\n--- Result of Data Collection ---")
    print(all_records)
    
    with open("capstone_weather_rawdata.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["city", "month", "metric", "temperature", "humidity", "pressure"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
    
        writer.writeheader()     
        writer.writerows(all_records)  
   
    print("\n Successfully saved to capstone_weather_rawdata.csv")

finally:
    driver.quit()