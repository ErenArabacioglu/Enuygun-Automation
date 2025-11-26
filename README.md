#  Enuygun Automation  
### Junior QA Engineer – Case Study Project

This repository contains an end-to-end automation framework developed for the **Wingie Enuygun Group – Junior QA Engineer Case Study**.  
The project automates flight search, filtering, data extraction, and data-driven analysis on **enuygun.com**, following a clean and scalable automation architecture.

It was developed using:

- **Python**
- **Selenium WebDriver**
- **PyTest**
- **Page Object Model (POM)**
- **OOP principles**
- **Custom logging, reporting, and configuration system**

---

##  Implemented Test Cases

Below are all implemented cases exactly as described in the Case Study requirements.

---

### ✅ **Case 1 – Basic Flight Search & Time Filter**

**Goals:**
- Perform round-trip flight search (Istanbul → Ankara)
- Read cities & dates from `config.ini`
- Apply "10:00–17:59" time filter
- Verify all departure times are within the selected range

---

### ✅ **Case 2 – Price Sorting for Turkish Airlines**

**Goals:**
- Apply time filter  
- Filter flights to **Turkish Airlines only**
- Validate:
  - All results belong to Turkish Airlines
  - Prices sorted correctly (ascending)
  - Sorting accuracy verified

---

### ✅ **Case 3 – Critical Path Testing**

**Goals:**
- One-way flight search (Istanbul → Ankara)
- Select first available flight
- Navigate to checkout page
- Validate checkout UI elements

---

### ✅ **Case 4 – Analysis and Categorization**

**The script automatically:**

✔ Extracts complete flight data:
- Departure/Arrival times  
- Airline name  
- Price  
- Flight duration  
- Connection info  

✔ Saves all flights to CSV  
✔ Calculates:
- Min / Max / Average prices by airline  
- Time-slot based price heatmap  
- Best flights (cheapest + shortest)

✔ Generates visualizations:
- `case4_avg_price_by_airline.png`
- `case4_price_heatmap.png`
- `case4_best_flights.csv`
- `case4_price_stats_by_airline.csv`

All stored under `/reports`.

---

##  Framework Features

- Page Object Model (POM)
- Reusable BasePage actions
- Clean OOP structure
- Centralized configuration (`config.ini`)
- Browser selection (Chrome / Firefox)
- Automatic screenshots for failed tests
- Custom logging system (`logs/test.log`)
- HTML reporting via **pytest-html**
- Error handling & clear assertions

---

##  How to Run the Tests


### **1. Run ALL tests + HTML report**
```
pytest -q --html=reports/test_report.html --self-contained-html
```

### **2. Run specific test**
```
pytest tests/test_basic_search_time_filter.py -q
```

