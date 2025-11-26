import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class ResultsPage(BasePage):
    flight_cards = (By.XPATH,"//*[starts-with(@id,'flight-')]")
    price_inside_card = ".//div[1]/div[1]/div/div[4]/div/span[1]"
    departure_time_on_card = (By.XPATH,".//div[@data-testid='departureTime']")
    airlines_filter_header = (By.XPATH,"//div[contains(@class, 'card-header')][.//span[normalize-space()='Havayolları']]")
    time_filter_section_header = (By.XPATH,"//*[@id='SearchRoot']/div[2]/div[2]/div[3]/div[4]/div[1]/span")
    noon_filter = (By.XPATH,"//*[@id='SearchRoot']/div[2]/div[2]/div[3]/div[4]/div[2]/div/div[1]/div[3]/p[3]")
    turkish_airlines_label = (By.XPATH,"//label[.//span[normalize-space()='Türk Hava Yolları']]")
    airline_name_on_card = (By.CSS_SELECTOR, "div.summary-marketing-airlines")
    first_flight_select_button = (By.CSS_SELECTOR, "button.action-select-btn")
    continue_button = (By.XPATH, "//*[@id='flight-0']/div[1]/div[6]/div[2]/button")
    arrival_time_on_card = (By.CSS_SELECTOR, "[data-testid='arrivalTime']")
    duration_on_card = (By.CSS_SELECTOR, "[data-testid='departureFlightTime']")
    connection_info_on_card = (By.CSS_SELECTOR, "[data-testid='transferStateTransfer']")

    def apply_time_filter_10_17(self):
        self.close_cookies_if_present()
        self.scroll_to_and_click(self.time_filter_section_header)
        time.sleep(1)
        self.scroll_to_and_click(self.noon_filter)
        time.sleep(2)

    def apply_turkish_airlines_filter(self):
        self.scroll_to(self.airlines_filter_header)
        self.scroll_to_and_click(self.airlines_filter_header)
        self.scroll_to_and_click(self.turkish_airlines_label)
        try:
            self.wait.until(
                EC.presence_of_all_elements_located(self.departure_time_on_card)
            )
        except TimeoutException:
            raise AssertionError("No flight results came up after the THY filter.")

    def get_all_departure_times(self):
        locator = self.departure_time_on_card
        for _ in range(3):  # max 3 deneme
            try:
                self.wait.until(EC.presence_of_all_elements_located(locator))
                elements = self.driver.find_elements(*locator)
                times = []
                for el in elements:
                    text = el.text.strip()
                    if text:
                        times.append(text)
                return times
            except StaleElementReferenceException:
                continue
        raise RuntimeError("Departure times could not be read due to stale elements.")

    def get_all_prices(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.departure_time_on_card))
        except TimeoutException:
            print("DEBUG: No result card found (departure_time_on_card does not exist)")
            return []
        prices = []
        for attempt in range(3):
            try:
                cards = self.driver.find_elements(*self.flight_cards)
                visible_cards = [c for c in cards if c.is_displayed()]
                print(f"DEBUG: visible flight cards = {len(visible_cards)}")
                prices.clear()
                for card in visible_cards:
                    try:
                        price_el = card.find_element(By.XPATH, self.price_inside_card)
                        text = price_el.text.strip()
                        if not text:
                            continue
                        clean = text.replace(".", "").replace(" ", "")
                        if clean.isdigit():
                            prices.append(int(clean))
                    except Exception:
                        continue
                print("DEBUG prices:", prices)
                return prices
            except StaleElementReferenceException:
                continue
        return []

    def get_all_airlines(self):
        locator = self.airline_name_on_card
        for attempt in range(3):
            try:
                elements = self.driver.find_elements(*locator)
                visible_elements = [el for el in elements if el.is_displayed()]
                names = []
                for el in visible_elements:
                    text = (el.text or "").strip()
                    if text:
                        names.append(text)
                print("DEBUG airlines:", names)
                return names
            except StaleElementReferenceException:
                continue
            except TimeoutException:
                print("DEBUG: airline element bulunamadı")
                return []
        return []

    def is_loaded(self, timeout: int = 15) -> bool:
        self.close_cookies_if_present()
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(self.flight_cards)
            )
            return True
        except TimeoutException:
            return False

    def has_flights(self, timeout: int = 15) -> bool:
        try:
            flights = WebDriverWait(self.driver, timeout).until(
                ec.presence_of_all_elements_located(self.flight_cards)
            )
            return len(flights) > 0
        except TimeoutException:
            return False

    def select_first_flight(self, timeout: int = 15):
        button = WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(self.first_flight_select_button)
        )
        button.click()

    def click_continue_button(self, timeout: int = 20):
        btn = WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(self.continue_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        self.driver.execute_script("arguments[0].click();", btn)

    def get_all_flights_data(self):
        self.logger.info("Collecting all flight cards data")
        self.close_cookies_if_present()
        cards = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_all_elements_located(self.flight_cards)
        )
        flights = []
        for card in cards:
            try:
                dep_time = card.find_element(*self.departure_time_on_card).text
            except:
                dep_time = ""
            try:
                arr_time = card.find_element(*self.arrival_time_on_card).text
            except:
                arr_time = ""
            try:
                airline = card.find_element(*self.airline_name_on_card).text
            except:
                airline = ""
            try:
                price_text = card.find_element(By.XPATH, self.price_inside_card).text
            except:
                price_text = ""

            digits = "".join(ch for ch in price_text if ch.isdigit())
            price = float(digits) if digits else 0.0
            try:
                connection = card.find_element(*self.connection_info_on_card).text
            except:
                connection = ""
            try:
                duration = card.find_element(*self.duration_on_card).text
            except:
                duration = ""

            flights.append({
                "departure_time": dep_time,
                "arrival_time": arr_time,
                "airline": airline,
                "price": price,
                "connection": connection,
                "duration": duration
            })
        self.logger.info(f"Collected {len(flights)} flights")
        return flights
