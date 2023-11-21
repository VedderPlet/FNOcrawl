import time
import constants
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Build driver to use for other pages
path = '/Users/tau/Documents/chromedriver'
s = Service(path)
driver = webdriver.Chrome(service=s)


def handle(elements, value: list):
    for element in elements:
        if element.text.strip() in value:
            # constant
            time.sleep(1)
            element.click()


# Prints page listings and sets
def get_page_listings():
    page_listings = 0
    all_apt = driver.find_element(By.CSS_SELECTOR, "div.switch-list-content")
    apts = all_apt.find_elements(By.CSS_SELECTOR, "section.vue-list-rent-item")

    for apt in apts:
        page_listings += 1

    print(f"{page_listings} page listings for page 1")
    return page_listings
