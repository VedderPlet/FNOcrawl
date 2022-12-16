import datetime
import re
from argparse import Action
from cgitb import text
from multiprocessing.connection import wait
from turtle import home
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
# windows use below
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.support.expected_conditions import staleness_of
from distutils.filelist import findall
import re
from xml.etree.ElementPath import find
import math

# website, chromedriver path setup

# Request Search Hour
uinput_hour = int(input("Enter numeric hour (1 - 24 hours) ex. '1' for '1 hour ago':"))

# request amount of listings from user
uresult_amount = int(input("Enter result crawl):"))

website = 'https://rent.591.com.tw/'
# Mac use below
path = '/Users/tau/Downloads/chromedriver'
# # deprecated
# # driver = webdriver.Chrome(path)
s = Service(path)
driver = webdriver.Chrome(service=s)

# Windows use below
# path = '/Users/taure/Downloads/WebScrape/chromedriver'
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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
# identify dropdown box element and identify all elements within to find city
links = driver.find_element(By.CSS_SELECTOR, "section.region-areabox-wrapper").find_elements(By.CSS_SELECTOR, "a")

# links = box.find_elements(By.CSS_SELECTOR, "a")
# time.sleep(2)
## Wait for all elements to load

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
page_number = 1


# Function to easily grab room custom selection and click each
def handle(elements, value: list):
    for element in elements:
        if element.text.strip() in value:
            element.click()

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
    value=["整層住家"])

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
    value=["可開伙", "有車位"])

# Add wait to make sure element is clickable
time.sleep(2)

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

# Input ping range, click ping button to complete search
input[2].send_keys("9")
input[3].send_keys("25")
inputbutton[1].click()

# Sort result table by new
handle(elements=driver
       .find_element(By.CSS_SELECTOR, 'div.switch-tips')
       .find_elements(By.CSS_SELECTOR, 'ul, li'),
       value=["最新"])

##test

# page_two = "2"
# handle(
#     elements=driver
#         .find_elements(By.CSS_SELECTOR, 'div.page-limit a'),
#     value=[f"{page_two}"])

# current date time
current_date = datetime.datetime.now()
# format is datetime.timedelta(
# days=0, seconds=0, microseconds=0,
# milliseconds=0, minutes=0, hours=0,
# weeks=0) Returns : Date

scrape_date = datetime.timedelta()

user_date_search = ((datetime.datetime.now()) - (datetime.timedelta(0, 0, 0, 0, 0, uinput_hour)))
print(user_date_search)

#Setting up
current_page = 1
page_load_limit = 30

# Find total number of listings on page
page_listings = 0
all_apt = driver.find_element(By.CSS_SELECTOR, "div.switch-list-content")
apts = all_apt.find_elements(By.CSS_SELECTOR, "section.vue-list-rent-item")

for apt in apts:
    page_listings += 1

print(f"{page_listings} page listings for page 1")

#Get whole pages to search through [70 pages request = 2 full pages of results]
page_max = (math.floor(uresult_amount / page_load_limit))

# partial pages to iterate through [70 pages = 10 items on 3rd page left to scrape]
remainder = (uresult_amount - (page_load_limit * page_max))


# page_listings = int(input("Enter available listings under 31 ")) 
page = "page element pressed"
listing_id = 0
# iterate through result list to find valid result
# note: This while loop determines date validity (within user request)
# after clicking on the post itself. Should be included in the if statements for user #of apartment request

def load_findings():

    # Find total number of listings on page 1
    page_listings = 0
    all_apt = driver.find_element(By.CSS_SELECTOR, "div.switch-list-content")
    apts = all_apt.find_elements(By.CSS_SELECTOR, "section.vue-list-rent-item")

    for apt in apts:
        page_listings += 1

    print(page_listings)

    invalid_result = []
    valid_result = []
    listing_id = 0
    loop_amount = 0

    #Check if user input is over 30, the max limit for available listings, if so set it to 30
    if uresult_amount > 30 and page_max and page_listings == 30:
        loop_amount = 30
        print(f"{loop_amount} is the loop amount, should be 30")

    elif uresult_amount > 30 and page_max and page_listings < 30:
        loop_amount = page_listings

    elif not page_max:
        loop_amount = remainder

    else: 
        loop_amount = uresult_amount
        print(f"{loop_amount} is the user input, should be under 30")
    

    while listing_id < loop_amount:
        print(f"{loop_amount} is Uresult in load_finding function")
        print(f"{listing_id} is listing ID")

        # load scraped post date into 2 sets of variables
        # first set is a calendar and day number
        format_month = 0
        format_day = 0

        # second set is days, minutes, hours, or seconds from current time
        format_days_ago = 0
        format_minutes_ago = 0
        format_hours_ago = 0
        format_seconds_ago = 0

        # Wait until first item is available
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.switch-list-content"))
        )

        # identify first item title then click it
        item_title = driver.find_elements(By.CSS_SELECTOR, 'div.item-title')[listing_id]
        item_title.click()
        print(f"{listing_id} loop")
        time.sleep(3)

        # Navigate to New tab opened with job post Selected,
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)

        # On new tab selected, find the created date
        creation_date = driver.find_element(
            By.XPATH, '//*[@id="rightConFixed"]/div/div[1]').get_attribute(
            "textContent").replace(" ", "")

        # print(creation_date)

        # Function for getting the number from character input
        def fn(s: str, month_year_min):
            s = ""
            pattern = f'([\d]+)({month_year_min})'
            match = re.search(pattern, creation_date)

            return match.group(1)

        if "月" in creation_date:

            # method implementation
            format_month += int(fn(creation_date, '月'))

            # method implementation
            format_day += int(fn(creation_date, '日'))

        elif "此房屋在剛剛發佈" in creation_date:

            format_seconds_ago += 1

        elif "天" in creation_date:

            format_days_ago += int(fn(creation_date, '天'))

        elif "小時" in creation_date:

            format_hours_ago += int(fn(creation_date, '小時'))

        elif "分鐘" in creation_date:

            format_minutes_ago += int(fn(creation_date, '分鐘'))

        else:
            print("Something is wrong check if statements")

        c_date = (format_month + format_day)
        d_value = (format_minutes_ago + format_hours_ago + format_seconds_ago + format_days_ago)

        # Return date of post creation if a calendar date was given,
        apt_creation_date = ""

        # may need to consider getting the year from the site
        if c_date > 0:
            apt_creation_date = datetime.datetime(2022, format_month, format_day)

        elif d_value > 0:
            apt_creation_date = (datetime.datetime.now()) - \
                                (datetime.timedelta(format_days_ago,
                                                    format_seconds_ago, 0, 0,
                                                    format_minutes_ago, format_hours_ago, 0))

        else:
            print("No date or time entered")

        if user_date_search <= apt_creation_date:
            valid_result.append(driver.current_url)
            listing_id += 1
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        elif user_date_search > apt_creation_date:
            invalid_result.append(driver.current_url)
            listing_id += 1
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    print(f"Valid results listed: {valid_result}")
    print(f"Invalid results listed: {invalid_result}")

##consider page greater than page 1 not present, consider no listing data on first page
#Put "load_listing" function from 591 in the big 3 here.

# PROBLEM: Unable to capture page listing amount for Page #2

if uresult_amount > 30 and page_listings == 30: 
    
        # whole pages to iterate through
    print(f"Maximum number of pages are/is {page_max}")
    
    # print results for all page results
    # Print all contents if request is over page load limit
    while page_max > 0 and page_listings == 30: 
        
        handle(elements=driver
        .find_elements(By.CSS_SELECTOR, "div.page-limit a"),
        value=[str(current_page)])

        page_listings = 0
        all_apt = driver.find_element(By.CSS_SELECTOR, "div.switch-list-content")
        apts = all_apt.find_elements(By.CSS_SELECTOR, "section.vue-list-rent-item")

        for apt in apts:
            page_listings += 1

        print(f"Now on page {current_page} with {page_listings} apartment listings")
    
        #return available listings for page
        load_findings()
        # while listing_id <= page_listings:
            
        #     print(f"creation date number {listing_id}")
        #     listing_id += 1
        
        #reset listing_id 
        listing_id = 0

        # CODE: Navigate to next page
        print(f"Page {current_page} completed")
        current_page += 1
        page_max -= 1

        

    # CODE: Navigate to page with remainder
    remainder_page_navigation = int((math.ceil(uresult_amount / page_load_limit)))

    #set remainder for listing ID 
    # listing_id = remainder

   
    print(f"Currently on Page {remainder_page_navigation}")
    # print(f"Remainder {listing_id} printed")

    #navigate to remainder page
    handle(elements=driver
    .find_elements(By.CSS_SELECTOR, "div.page-limit a"),
    value=[str(remainder_page_navigation)])

    load_findings()
    listing_id = 0
    # listing_id += 1
    # remainder -= 1
    
elif uresult_amount > page_listings and 0 < page_listings < 30:

    listing_id = page_listings
    load_findings()

    # while listing_id <= page_listings:
    #     print("Page 1")
    #     print(f"Creation date number {listing_id} printed")
    #     listing_id += 1
    listing_id = 1

elif uresult_amount <= 30 and uresult_amount <= page_listings:

    if uresult_amount <= 0:
        print("No data available")

    print(f"{listing_id} = listing id")
    print(f"{uresult_amount} = result amount")
    load_findings()

    # while listing_id <= uresult_amount:
    #     print("Page 1")
    #     print(listing_id)
    #     listing_id += 1 
    listing_id = 1

elif page_listings < 1:
    print("No listings available")

else:
    print("No data available")

# ##organize above

# https://github.com/line/line-bot-sdk-python (send listings to line app) (complex, use it later once comfortable)
# Or use Gmail API https://www.thepythoncode.com/article/use-gmail-api-in-python

# Wait for 5 seconds, then close out Google Chrome
time.sleep(5)

# driver.close()
driver.quit()
