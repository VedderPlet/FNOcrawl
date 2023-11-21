import datetime
from asyncio import constants
from date_data import string_to_datetime
import user_input
import constants
from constants import driver, time, element_wait, By
import utils
from loop_listings import set_loop_amount
import math
from utils import handle


# May need to include paging with this

def load_findings(user_date_search: datetime.datetime, uresult_amount: int, page_max: int, remainder: int, page_listings: int):
    listing_id = constants.listing_id

    utils.get_page_listings()

    # This is just logging
    # print(page_max, True if page_max else False)
    # print(f"{uresult_amount} should be reset on remainder run")
    # Determines loop amount based on amount requested and what is available per page
    loop_amount = set_loop_amount(uresult_amount, page_max, page_listings, remainder)

    while listing_id < loop_amount:
        print(f"{loop_amount} is Uresult in load_finding function")
        print(f"{listing_id} is listing ID")

        element_wait()

        # identify first item title then click it
        item_title = driver.find_elements(By.CSS_SELECTOR, 'div.item-title')[listing_id]
        item_title.click()
        print(f"{listing_id} loop")

        # Constant
        time.sleep(3)

        # Navigate to New tab opened with job post Selected,
        # Constant New Tab Navigation
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)

        # On new tab selected, find the created date
        creation_date = driver.find_element(
            By.XPATH, '//*[@id="rightConFixed"]/div/div[1]').get_attribute(
            "textContent").replace(" ", "")

        # Get date from 591 and convert it to a datetime to fetch valid listings

        final_valid_result = []
        final_invalid_result = []

        print(creation_date,user_date_search, string_to_datetime(creation_date))

        if user_date_search <= string_to_datetime(creation_date):
            final_valid_result.append(driver.current_url)
            listing_id += 1
            driver.close()

            # Constant, switch to original window
            driver.switch_to.window(driver.window_handles[0])
        else:
            final_invalid_result.append(driver.current_url)
            listing_id += 1
            driver.close()

            # Constant, switch to original window
            driver.switch_to.window(driver.window_handles[0])

        return final_valid_result, final_invalid_result


def page_scrape(user_date_search: datetime.datetime, uresult_amount: int, page_max: int, remainder: int, page_listings: int):
    c_page = constants.current_page
    p_max = page_max
    u_amount = uresult_amount
    p_l_limit = constants.page_load_limit
    valid_result = []
    invalid_result = []

    if uresult_amount > 30 and page_listings == 30:

        # whole pages to iterate through
        print(f"Maximum number of pages are/is {p_max}")

        # print results for all page results
        # Print all contents if request is over page load limit
        while page_max > 0 and page_listings == 30:

            # should be in utils (If the function will be used in other areas,
            handle(elements=driver
                   .find_elements(By.CSS_SELECTOR, "div.page-limit a"),
                   value=[str(c_page)])

            page_listings = 0
            all_apt = driver.find_element(By.CSS_SELECTOR, "div.switch-list-content")
            apts = all_apt.find_elements(By.CSS_SELECTOR, "section.vue-list-rent-item")

            for apt in apts:
                page_listings += 1

            print(f"Now on page {c_page} with {page_listings} apartment listings")

            # return available listings
            valid, invalids = load_findings(user_date_search, page_max=page_max, remainder=remainder, uresult_amount=uresult_amount, page_listings=page_listings)
            valid_result.append(valid)
            invalid_result.append(invalid_result)
            listing_id = 0

            # CODE: Navigate to next page
            print(f"Page {c_page} completed")
            c_page += 1
            p_max -= 1

        # CODE: Navigate to page with remainder
        remainder_page_navigation = int((math.ceil(u_amount / p_l_limit)))

        print(f"Currently on Remainder Page {remainder_page_navigation}")
        # print(f"Remainder {listing_id} printed")

        # navigate to remainder page
        handle(elements=driver
               .find_elements(By.CSS_SELECTOR, "div.page-limit a"),
               value=[str(remainder_page_navigation)])

        time.sleep(5)

        # reset uresult amount to remainder
        user_input.uresult_amount = remainder
        print(f"{uresult_amount} is the new result amount (should equal remainder)")
        valid, invalids = load_findings(user_date_search, page_max=page_max, remainder=remainder,
                                        uresult_amount=uresult_amount, page_listings=page_listings)
        valid_result.append(valid)
        invalid_result.append(invalid_result)
        listing_id = 0
        return valid_result, invalid_result
    else:
        return load_findings(user_date_search, page_max=page_max, remainder=remainder, uresult_amount=uresult_amount, page_listings=page_listings)
