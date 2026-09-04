# This code is for cleaning the raw weather data collected from scraping_weather.py. 

import pandas as pd
import calendar

# Load the raw data from the CSV file
raw_data = pd.read_csv("capstone_weather_rawdata.csv")

# print the first few rows of the raw data to understand its structure
print("\n--- Raw Data Preview ---")
print(raw_data.head())

print("\n--- Data Info ---")
print(raw_data.info())


print("--------- Summary and Plan ---------")
print("1. We don't have any missing values in the dataset.")
print("2. The 'temperature', 'humidity', and 'pressure' columns are currently of type object (string). We need to convert them to numeric types for analysis and remove non-numeric characters.")
print("3. We will rename the columns to more descriptive names for clarity.")
print("4. We will add the 'year' column to the dataset, which will be set to 2025 for all records.")
print("5. We will add the name of the month in English to the dataset based on the 'month' column.")


# Start cleaning the data
df = raw_data.copy()

# 2-3. Convert the 'temperature', 'humidity', and 'pressure' columns to numeric types, removing non-numeric characters
df['temp_f'] = df['temperature'].str.extract(r'(-?\d+)').astype(float)
df['humidity_pct'] = df['humidity'].str.extract(r'(-?\d+)').astype(float)
df['pressure_inHg'] = df['pressure'].str.extract(r'(\d+\.?\d*)').astype(float)

# 4. Add the 'year' column 
df['year'] = 2025

# 5. Add the name of the month in English based on the 'month' column
df['month_name'] = df['month'].apply(lambda x: calendar.month_name[int(x)])

print("\n--- Data After Conversion ---")
print(df.head())
print("\n--- Data Info After Conversion ---")
print(df.info())

print(" --------- Temporary results: ---------")
print("1. The 'temperature', 'humidity', and 'pressure' columns have been successfully converted to numeric types.")
print("2. The 'year' column has been added with the value 2025 for all records.")
print("3. The 'month_name' column has been added with the English names of the months based on the 'month' column.")
print("Finally, we will take city month, month_name, year, metric, temp_f, humidity_pct, pressure_inHg columns and save the cleaned data to a new CSV file.\n")

# Define the columns to keep in the cleaned dataset
clean_columns = [
    'city',
    'year',
    'month',
    'month_name',
    'metric',
    'temp_f',
    'humidity_pct',
    'pressure_inHg'
]

df_clean = df[clean_columns]

# Check the cleaned data
print("--- Clean Data Preview ---")
print(df_clean.head(10))
print("\n--- Data Types ---")
print(df_clean.dtypes)

# Save the cleaned dataset
df_clean.to_csv("capstone_weather_cleaned.csv", index=False)
print("\nFile capstone_weather_cleaned.csv saved successfully.")