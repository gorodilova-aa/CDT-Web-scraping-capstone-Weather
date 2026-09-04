# CDT Web Scraping Capstone: Weather Comparison

## Overview
This project compares historical weather data for the year 2025 between two geographically distinct locations:
- **Raleigh, NC, USA** (Humid subtropical climate)
- **Novosibirsk, Russia** (Humid continental / subarctic climate)

The project extracts data from the web using automated browser tooling, cleans and standardizes the dataset, and prepares it for analysis and visualization.

---

## Project Structure
- `scraping_weather.py` — Scrapes monthly historical weather summaries (High, Low, Average) for both cities via Selenium and saves raw output to `capstone_weather_rawdata.csv`.
- `cleaning_weather.py` — Cleans raw text fields, extracts numeric values (temperatures, humidity, barometric pressure), adds standardized metadata (calendar month names, year), and saves cleaned output to `capstone_weather_cleaned.csv`.
- `capstone_weather_rawdata.csv` — Raw scraped data file.
- `capstone_weather_cleaned.csv` — Cleaned and transformed dataset ready for analysis.

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/CDT-Web-scraping-capstone-Weather.git
   cd CDT-Web-scraping-capstone-Weather
2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
3. **Install dependencies:**
    ```bash 
    pip install selenium webdriver-manager pandas

---

## How to Run

1. **Scrape raw data**
    ```bash
    python scraping_weather.py

2. **Clean and transform data**
    ```bash
    python cleaning_weather.py