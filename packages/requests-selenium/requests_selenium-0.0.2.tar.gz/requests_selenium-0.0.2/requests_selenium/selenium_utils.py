import time
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class requests_selenium:
    '''
    usage:

    html_source = requests_selenium.get(url)

    driver = requests_selenium.get_driver()
    '''
    driver = None  # Class-level attribute to store the driver

    @staticmethod
    def get(url, headless=True, wait_time=5):
        chromedriver_autoinstaller.install()

        # Configure options based on headless mode
        options = Options()
        if headless:
            options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        requests_selenium.driver = driver  # Store the driver in the class attribute

        driver.get(url)
        time.sleep(wait_time)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup

    @staticmethod
    def get_driver(headless=True):
        chromedriver_autoinstaller.install()

        # Configure options based on headless mode
        options = Options()
        if headless:
            options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        requests_selenium.driver = driver  # Store the driver in the class attribute

        return driver
