import configparser
import os
import pytest
from pages.home_page import HomePage
from pages.results_page import ResultsPage
from utils.logger import get_logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, "config", "config.ini")
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

@pytest.mark.case1
def test_basic_flight_search_with_time_filter(driver):
    logger = get_logger("CASE1")
    logger.info("CASE 1 – Starting basic flight search test")
    home = HomePage(driver)
    results = ResultsPage(driver)
    from_city = config["search"]["default_from"]
    to_city = config["search"]["default_to"]
    dep_date = config["search"]["default_departure_date"]
    ret_date = config["search"]["default_return_date"]
    home.search_round_trip(from_city, to_city, dep_date, ret_date)
    results.apply_time_filter_10_17()
    departure_times = results.get_all_departure_times()
    assert len(departure_times) > 0, "No flight results found."
    for t in departure_times:
        hour, minute = map(int, t.split(":"))
        total_minutes = hour * 60 + minute
        assert 10 * 60 <= total_minutes <= 17 * 60 + 59, f"time out of range: {t}"

    logger.info("CASE 1 – Test completed successfully")