import os
import pytest
from utils.logger import get_logger
from pages.home_page import HomePage
from pages.results_page import ResultsPage
import configparser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, "config", "config.ini")
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

@pytest.mark.case2
def test_price_sorting_for_turkish_airlines(driver):
    logger = get_logger("CASE2")
    logger.info("CASE 2 – Starting price sorting for Turkish Airlines test")
    home = HomePage(driver)
    results = ResultsPage(driver)

    from_city = config["search"]["default_from"]
    to_city = config["search"]["default_to"]
    dep_date = config["search"]["default_departure_date"]
    ret_date = config["search"]["default_return_date"]

    home.search_round_trip(from_city, to_city, dep_date, ret_date)
    results.apply_time_filter_10_17()
    results.apply_turkish_airlines_filter()
    prices = results.get_all_prices()
    assert len(prices) > 0, "No flight results found after applying the THY filter."
    assert prices == sorted(prices), f"Prices are not in ascending order: {prices}"

    airline_names = results.get_all_airlines()
    assert len(airline_names) > 0, "THY filtresinden sonra havayolu ismi bulunamadı."
    print(f"DEBUG airline count = {len(airline_names)}, price count = {len(prices)}")

    for name in airline_names:
        normalized = name.lower()
        assert (
                "türk hava yolları" in normalized
                or "turkish airlines" in normalized
                or "thy" in normalized
        ), f"An airline other than THY was found on the list.: {name}"

    logger.info("CASE 2 – Test completed successfully")