import sqlite3
import pandas as pd



df = pd.read_csv("capstone_weather_cleaned.csv")

# Define the database path
db_path = "capstone_weather.db"

try:
    with sqlite3.connect(db_path) as conn:
        df.to_sql(
            name="weather_records",
            con=conn,
            if_exists="replace",
            index=False
        )
    print("\n--- Table 'weather_records' successfully added to database 'capstone_weather.db'. --- ")

    # Check the inserted data
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_records LIMIT 5")
    print("\n--- Check the inserted data: First 5 rows from the database: ---")
    for row in cursor.fetchall():
        print(row)


except sqlite3.Error as e:
    print(f"Database error: {e}")

# close the connection
conn.close()