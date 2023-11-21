import datetime
from apartment_loader import load_findings, page_scrape
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import math
from user_input import get_user_input, parse_date_start_search, parse_listing_total
from constants import website
from utils import driver
from constants import page_load_limit

# website, chromedriver path setup

# Request Search Hour
user_date_search = parse_date_start_search(get_user_input("Enter number of hours in the past to scrape for listings: "))
uresult_amount = parse_listing_total(get_user_input("Enter number of results to scrape: "))

# Get whole pages to search through [70 pages request = 2 full pages of results]
page_max = (math.floor(uresult_amount / page_load_limit))

# partial pages to iterate through [70 pages = 10 items on 3rd page left to scrape]
remainder = (uresult_amount - (page_load_limit * page_max))

final_valid_result = []
final_invalid_result = []

# Windows use below
# path = '/Users/taure/Downloads/WebScrape/chromedriver'
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

##consider constants.py for variables that shouldn't change
driver.implicitly_wait(5)
print("Implicit wait completed")

# Get website access
driver.get(website)

# Hover action, home page region button location setup
region_button = driver.find_element(By.CSS_SELECTOR, "div.new-search-region")
need_to_hover = ActionChains(driver=driver).move_to_element(region_button)
home_page = driver.find_element(By.CSS_SELECTOR, "div.rent-list-container")

# hover to show region dropdown [on]

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.vue-list-new-head"))
)

need_to_hover.perform()
print("Hovering")

# constant
time.sleep(1)

# identify dropdown box element and identify all elements within to find city
links = driver.find_element(By.CSS_SELECTOR, "section.region-areabox-wrapper").find_elements(By.CSS_SELECTOR, "a")

# links = box.find_elements(By.CSS_SELECTOR, "a")
# time.sleep(2)
# Wait for all elements to load

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.vue-filter-container"))
)

# iterate through list to find specific city
for link in links:
    if link.text.strip() == '新北市':
        # print(link.get_attribute("outerHTML"))
        link.click()

# Click homepage to close region dropdown
driver.implicitly_wait(3)

home_page.click()
print("Home Page clicked")

# Constant
page_number = 1


# Function to grab room custom selection and click each
def handle(elements, value: list):
    for element in elements:
        if element.text.strip() in value:
            # constant
            time.sleep(1)
            element.click()


#  Look into config ----
# config = [{
#     'list': driver
#     .find_elements(By.CSS_SELECTOR, 'button.statement-confirm'),
#     'value': 'agree'
# }, {
#
# }]
#
# for c in config:
#     handle(c.list, value=c.value)

handle(
    elements=driver
    .find_elements(By.CSS_SELECTOR, 'button.statement-confirm'),
    value=["同意"])

handle(
    elements=driver
    .find_elements(By.CSS_SELECTOR, "ul.town-list.clearfix li"),
    value=["不限"])

handle(
    elements=driver
    .find_elements(By.CSS_SELECTOR, '.vue-filter-list-item')[0]
    .find_elements(By.CSS_SELECTOR, 'ul li'),
    value=["不限"])

handle(
    elements=driver
    .find_elements(By.CSS_SELECTOR, '.vue-filter-list-item')[2]
    .find_elements(By.CSS_SELECTOR, 'ul, li'),
    value=["不限"])

handle(
    elements=driver
    .find_elements(By.CSS_SELECTOR, '.vue-filter-list-item')[2]
    .find_elements(By.CSS_SELECTOR, 'ul, li'),
    value=["1房"])

handle(
    elements=driver
    .find_elements(By.CSS_SELECTOR, '.vue-filter-list-item')[3]
    .find_elements(By.CSS_SELECTOR, 'ul li'),
    value=["可開伙"])

# Add wait to make sure element is clickable
# time.sleep(5)
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.vue-filter-container"))
)

input = driver.find_elements(By.CSS_SELECTOR, 'input.filter-custom-input')
input[0].send_keys("8000")
input[1].send_keys("90000")
inputbutton = driver.find_elements(By.CSS_SELECTOR, 'button.filter-custom-submit')
inputbutton[0].click()

# Expand table by clicking text area
handle(
    elements=driver
    .find_element(By.CSS_SELECTOR, 'div.show-more')
    .find_elements(By.CSS_SELECTOR, 'div span'),
    value=["(型態/坪數/樓層/設備/須知)"])

# Select "elevator building" checkbox
handle(
    elements=driver
    .find_elements(By.CSS_SELECTOR, '.vue-filter-list-item')[4]
    .find_elements(By.CSS_SELECTOR, 'ul, li'),
    value=["電梯大樓"])

handle(
    elements=driver
    .find_elements(By.CSS_SELECTOR, '.vue-filter-list-item')[7]
    .find_elements(By.CSS_SELECTOR, 'ul, li'),
    value=["有洗衣機"])

# Input ping range, click ping button to complete search
input[2].send_keys("20")
input[3].send_keys("90")
inputbutton[1].click()

# Sort result table by new
handle(elements=driver
       .find_element(By.CSS_SELECTOR, 'div.switch-tips')
       .find_elements(By.CSS_SELECTOR, 'ul, li'),
       value=["最新"])

# constant
current_date = datetime.datetime.now()

scrape_date = datetime.timedelta()

print(user_date_search)

# Setting up / constants
current_page = 1
page_load_limit = 30

# CONSTANT
time.sleep(3)

# Find total number of listings on page
page_listings = 0
all_apt = driver.find_element(By.CSS_SELECTOR, "div.switch-list-content")
apts = all_apt.find_elements(By.CSS_SELECTOR, "section.vue-list-rent-item")

for apt in apts:
    page_listings += 1

print(f"{page_listings} page listings for page 1")

# Get whole pages to search through [70 pages request = 2 full pages of results]
page_max = (math.floor(uresult_amount / page_load_limit))

# partial pages to iterate through [70 pages = 10 items on 3rd page left to scrape]
remainder = (uresult_amount - (page_load_limit * page_max))

# page_listings = int(input("Enter available listings under 31 "))
page = "page element pressed"
listing_id = 0

# pages
# load_findings(user_date_search, uresult_amount, page_max, remainder, page_listings)
final_valid_result, final_invalid_result = page_scrape(user_date_search, uresult_amount, page_max, remainder, page_listings)


# https://github.com/line/line-bot-sdk-python (send listings to line app) (complex, use it later once comfortable)
# Or use Gmail API https://www.thepythoncode.com/article/use-gmail-api-in-python


print(f"Valid results listed: {final_valid_result}")
print(f"Invalid results listed: {final_invalid_result}")

# Wait for 5 seconds, then close out Google Chrome / Constant
time.sleep(5)

# driver.close()
driver.quit()

# check if mac or windows (python) check OS.