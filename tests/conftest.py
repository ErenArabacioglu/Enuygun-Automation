import os
import pytest
import configparser
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, "config", "config.ini")
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=config["env"]["browser"])

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    if browser == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    elif browser == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    driver.maximize_window()
    driver.implicitly_wait(int(config["env"]["implicit_wait"]))
    yield driver

    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"screenshots/{request.node.name}_{timestamp}.png"
        driver.save_screenshot(file_name)
        print(f"\n[SCREENSHOT SAVED] {file_name}")
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
