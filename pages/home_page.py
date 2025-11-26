import configparser
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, "config", "config.ini")
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")


class HomePage(BasePage):
    base_url = config["env"]["base_url"]
    from_input = (By.XPATH,"//label[@data-testid='flight-origin-input-comp']//input")
    to_input = (By.XPATH,"//label[@data-testid='flight-destination-input-comp']//input")
    popular_from_istanbul = (By.XPATH,"//button[contains(@data-testid, 'flight-search-popular-item-origin')]""[.//span[contains(normalize-space(), 'İstanbul')]]")
    popular_to_ankara = (By.XPATH,"//button[contains(@data-testid, 'flight-search-popular-item-destination')]""[.//span[contains(normalize-space(), 'Ankara')]]")
    departure_date_field = (By.XPATH,"//div[@data-testid='enuygun-homepage-flight-departureDate-label']")
    return_date_field = (By.XPATH,"//div[@data-testid='enuygun-homepage-flight-returnDate-label']")
    search_button = (By.XPATH,"//button[@data-testid='enuygun-homepage-flight-submitButton']")
    hotels_label = (By.XPATH,"//label[.//div[contains(., 'Bu tarihler için otelleri de listele')]]")

    def open_home(self):
        self.open(self.base_url)

    def is_hotels_checked(self) -> bool:
        return bool(
            self.driver.find_elements(
                By.CSS_SELECTOR,
                "span[data-testid*='flight-oneWayCheckbox-checked-span']"
            )
        )

    def ensure_hotels_unchecked(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.hotels_label))
            if self.is_hotels_checked():
                label_el = self.driver.find_element(*self.hotels_label)
                label_el.click()
        except TimeoutException:
            pass

    def set_from_city(self, city: str):
        self.logger.info(f"Setting FROM city: {city}")
        self.click(self.from_input)
        self.click(self.popular_from_istanbul)

    def set_to_city(self, city: str):
        self.logger.info(f"Setting TO city dynamically: {city}")
        self.click(self.to_input)
        self.click(self.popular_to_ankara)

    def set_to_city_dynamic(self, city_name: str):
        self.click(self.to_input)
        self.type(self.to_input, city_name)
        suggestion_locator = (By.CSS_SELECTOR, "div[data-testid^='autosuggestion-custom-item']")
        suggestions = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located(suggestion_locator)
        )
        suggestions[0].click()


    def select_date(self, date_str: str):
        date_xpath = f"//button[@title='{date_str}']"
        self.click((By.XPATH, date_xpath))

    def set_dates(self, departure_date: str, return_date: str):
        self.click(self.departure_date_field)
        self.select_date(departure_date)
        self.click(self.return_date_field)
        self.select_date(return_date)

    def set_departure_date(self, departure_date: str):
        self.click(self.departure_date_field)
        self.select_date(departure_date)

    def click_search(self):
        self.logger.info("Clicking 'Search' button")
        self.click(self.search_button)

    def search_round_trip(self, from_city: str, to_city: str,departure_date: str,return_date: str):
        self.open_home()
        self.close_cookies_if_present()
        self.set_from_city(from_city)
        self.set_to_city(to_city)
        self.set_dates(departure_date, return_date)
        self.ensure_hotels_unchecked()
        self.click_search()

    def search_one_way(self, from_city, to_city, dep_date):
        self.open_home()
        self.close_cookies_if_present()
        self.set_from_city(from_city)
        self.set_to_city(to_city)
        self.set_departure_date(dep_date)
        self.ensure_hotels_unchecked()
        self.click_search()

    def search_one_way_dynamic(self, from_city, to_city, dep_date):
        self.logger.info(f"Searching one-way {from_city} -> {to_city} on {dep_date}")
        self.open_home()
        self.close_cookies_if_present()
        self.set_from_city(from_city)
        self.set_to_city_dynamic(to_city)
        self.set_departure_date(dep_date)
        self.ensure_hotels_unchecked()
        self.click_search()