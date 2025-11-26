from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class CheckoutPage(BasePage):
    contact_info_title = (By.XPATH,"//*[contains(text(),'İletişim Bilgileri')]")
    adult_section_title = (By.XPATH,"//*[contains(text(),'Yetişkin')]")

    def is_loaded(self, timeout: int = 15) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(self.contact_info_title)
            )
            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(self.adult_section_title)
            )
            return True
        except TimeoutException:
            return False
