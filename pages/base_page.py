from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from utils.logger import get_logger


class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.logger = get_logger(self.__class__.__name__)
        self.wait = WebDriverWait(driver, timeout)

    def close_cookies_if_present(self):
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[normalize-space()='KABUL ET']")
                )
            )
            btn.click()
        except TimeoutException:
            pass

    def open(self, url):
        self.logger.info("Opening home page")
        self.driver.get(url)

    def scroll_to(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )
        return element

    def click(self, locator):
        self.logger.info(f"Clicking element: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def scroll_to_and_click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        element.click()

    def type(self, locator, text, clear=True):
        self.logger.info(f"Typing into {locator}: {text}")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def scroll_into_view(self, locator):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def wait_for_visibility(self, locator):
        self.logger.info(f"Waiting for visibility of: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
