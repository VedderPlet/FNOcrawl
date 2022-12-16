from distutils.filelist import findall
import re
from xml.etree.ElementPath import find
import math

#fix uresult > max items
current_page = 1
crawl_request = int(input("Enter number of apt to crawl "))
page_load_limit = 30

#Get whole pages to search through [70 pages request = 2 full pages of results]
page_max = (math.floor(crawl_request / page_load_limit))

# partial pages to iterate through [70 pages = 10 items on 3rd page left to scrape]
remainder = (crawl_request - (page_load_limit * page_max))

available_listings = int(input("Enter available listings under 31 ")) 
page = "page element pressed"
listing_id = 1

##consider page greater than page 1 not present, consider no listing data on first page
#Put "load_listing" function from 591 in the big 3 here.

if crawl_request > 30 and available_listings == 30: 
    # whole pages to iterate through
    print(page_max)
    # print results for all page results
    # Print all contents if request is over page load limit
    while page_max > 0:
        print(f"Now on page {current_page}")

        #return available listings for page
        while listing_id <= available_listings:
            print(f"creation date number {listing_id}")
            listing_id += 1
        
        
        #reset listing_id 
        listing_id = 1

        # CODE: Navigate to next page
        print(f"Page {current_page} completed")
        current_page += 1
        page_max -= 1

    # CODE: Navigate to page with remainder
    remainder_page_navigation = int((math.ceil(crawl_request / page_load_limit)))

    while remainder > 0:
        print(f"Currently on Page {remainder_page_navigation}")
        print(f"Remainder {listing_id} printed")
        listing_id += 1
        remainder -= 1
    
elif crawl_request > available_listings and 0 < available_listings < 30:
    while listing_id <= available_listings:
        print("Page 1")
        print(f"Creation date number {listing_id} printed")
        listing_id += 1
    listing_id = 1

elif crawl_request <= 30 and crawl_request <= available_listings:

    if crawl_request <= 0:
        print("No data available")

    while listing_id <= crawl_request:
        print("Page 1")
        print(listing_id)
        listing_id += 1 

elif available_listings < 1:
    print("No listings available")
else:
    print("No data available")

