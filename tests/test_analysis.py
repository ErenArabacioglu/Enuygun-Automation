import csv
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from utils.logger import get_logger
from pages.home_page import HomePage
from pages.results_page import ResultsPage
import configparser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, "config", "config.ini")
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

def test_analysis_istanbul_to_nicosia(driver):
    logger = get_logger("CASE4")
    logger.info("CASE 4 – Starting analysis test")
    home = HomePage(driver)
    results = ResultsPage(driver)
    from_city = config["analysis"]["from_city"]
    to_city = config["analysis"]["to_city"]
    dep_date = config["analysis"]["departure_date"]
    home.search_one_way_dynamic(from_city, to_city, dep_date)
    flights_data = results.get_all_flights_data()
    assert len(flights_data) > 0, "No flights found, no records to analyze!"

    filename = f"data/flights_{from_city}_{to_city}_{datetime.now():%Y%m%d_%H%M}.csv"
    os.makedirs("data", exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=flights_data[0].keys())
        writer.writeheader()
        writer.writerows(flights_data)

    print(f"\n[CASE4] Saved flight data to: {filename}")
    df = pd.DataFrame(flights_data)
    stats = df.groupby("airline")["price"].agg(["min", "max", "mean"])
    os.makedirs("reports", exist_ok=True)
    stats.to_csv("reports/case4_price_stats_by_airline.csv")
    plt.figure()
    stats["mean"].plot(kind="bar")
    plt.xlabel("Airline")
    plt.ylabel("Average Price (TRY)")
    plt.title("Average Flight Prices by Airline")
    plt.tight_layout()
    plt.savefig("reports/case4_avg_price_by_airline.png")
    plt.close()
    df["dep_hour"] = pd.to_datetime(df["departure_time"], format="%H:%M").dt.hour

    def slot(h):
        if 0 <= h < 6: return "00-06"
        if 6 <= h < 12: return "06-12"
        if 12 <= h < 18: return "12-18"
        return "18-24"

    df["time_slot"] = df["dep_hour"].apply(slot)
    pivot = df.pivot_table(
        index="airline",
        columns="time_slot",
        values="price",
        aggfunc="mean"
    )
    plt.figure()
    plt.imshow(pivot, aspect="auto")
    plt.xticks(range(len(pivot.columns)), pivot.columns)
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.colorbar(label="Average Price (TRY)")
    plt.title("Price Distribution by Time Slot and Airline")
    plt.tight_layout()
    plt.savefig("reports/case4_price_heatmap.png")
    plt.close()
    best_flights = df.sort_values("price").head(5)
    best_flights.to_csv("reports/case4_best_flights.csv", index=False)

    logger.info("CASE 4 – Test completed successfully")

