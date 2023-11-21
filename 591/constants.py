# CONSTANTS
import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait
from utils import driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

website = 'https://rent.591.com.tw/'
page_number = 1
current_date = datetime.datetime.now()
current_page = 1
page_load_limit = 30
listing_id = 0

TIME_SLEEP = 1

#CONSTANTS ARE JUST VARIABLES
def sleep():
    time.sleep(TIME_SLEEP)


def element_wait():
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.vue-list-new-head"))
    )
