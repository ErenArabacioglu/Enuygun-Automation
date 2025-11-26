Enuygun Automation – Wingie Enuygun Group
Junior QA Engineer – Case Study Project

This repository contains an end-to-end automation framework developed for the Wingie Enuygun Group – Junior QA Engineer Case Study.
The project automates flight search, filtering, data collection, and data-driven analysis on enuygun.com, using a clean and scalable automation architecture.

It was developed using:

Python
Selenium WebDriver
PyTest
Page Object Model (POM)
OOP principles
Custom logging, reporting, and configuration system

Implemented Test Cases
Below are all implemented cases, exactly as described in the Case Study document

Case 1 – Basic Flight Search & Time Filter

Goal: Verify that search results match selected parameters and flight times fall between 10:00–17:59.

Checks performed:

Round-trip search (Istanbul → Ankara)

Cities & dates read from config.ini

Time filter applied (10:00–17:59)

All departure times validated against range

Flight results successfully loaded

✅ Case 2 – Price Sorting for Turkish Airlines

Goal: Validate sorting accuracy for a specific airline.

Checks performed:

Apply time filter

Filter flights to Turkish Airlines only

Validate:

All flights belong to Turkish Airlines

Prices are sorted in ascending order

Sorting accuracy repeated & verified

✅ Case 3 – Critical Path Testing

Critical user journey automated:

Istanbul → Ankara one-way search

Select first available flight

Navigate to checkout page

Validate checkout UI elements (Passenger info, payment section, etc.)

✅ Case 4 – Data Extraction, Analysis & Categorization

Goal: Perform data analysis on Istanbul → Nicosia flights.

The script:

✔ Extracts all flight data:

Departure / Arrival times

Airline name

Price

Connection info

Flight duration

✔ Saves all flights to CSV

Stored under data/

✔ Generates analytics:

Min, Max, Average price by airline → CSV + Bar Chart

Price distribution heatmap by time slots (00–06, 06–12, 12–18, 18–24)

Best flights (cheapest + shortest) → CSV

✔ Visual outputs (stored in /reports):

case4_avg_price_by_airline.png

case4_price_heatmap.png

case4_best_flights.csv

case4_price_stats_by_airline.csv

🏗️ Framework Features

✔ Page Object Model (POM)
✔ Reusable BasePage methods
✔ Selenium WebDriver with dynamic waits
✔ Full logging system (logs/test.log)
✔ Automatic screenshots on failures
✔ Configurable browser (Chrome / Firefox)
✔ HTML reporting via pytest-html
✔ Clean code & OOP principles
✔ Error handling & assertion strategy

(All features required in Case Study PDF – Technical Requirements, Page 3)

▶️ How to Run the Tests
1. Install dependencies
pip install -r requirements.txt

2. Run all tests
pytest -q --html=reports/test_report.html --self-contained-html

3. Run a specific test

Example (Case 1):

pytest tests/test_basic_search_time_filter.py -q

🧪 HTML Test Report

After running tests, the HTML report will be generated at:

/reports/test_report.html


Includes:

Pass/Fail summary

Screenshots for failures

Environment metadata
