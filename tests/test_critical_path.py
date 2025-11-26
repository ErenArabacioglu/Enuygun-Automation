import os
from pages.home_page import HomePage
from pages.results_page import ResultsPage
from pages.checkout_page import CheckoutPage  # varsa; yoksa sonra ekleriz
import configparser
from utils.logger import get_logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, "config", "config.ini")
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

def test_critical_flight_journey(driver):
    logger = get_logger("CASE3")
    logger.info("CASE 3 – Starting critical path test")
    home = HomePage(driver)
    results = ResultsPage(driver)
    checkout = CheckoutPage(driver)

    from_city = config["search"]["default_from"]
    to_city = config["search"]["default_to"]
    dep_date = config["search"]["default_departure_date"]

    home.search_one_way(from_city, to_city, dep_date)
    assert results.is_loaded(), "Flight results page not loaded!"
    assert results.has_flights(), "The flight list came up empty!"
    results.select_first_flight()
    results.click_continue_button()
    assert checkout.is_loaded(), "Checkout / Passenger information page not loaded!"

    logger.info("CASE 3 – Test completed successfully")