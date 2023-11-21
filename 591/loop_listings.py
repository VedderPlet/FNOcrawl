def set_loop_amount(u: int, pm: int, pl: int, r: int) -> int:
    uresult_amount = u
    page_max = pm
    page_listings = pl
    remainder = r

    # Returns a full page of listings
    if uresult_amount == 30 or page_max and page_listings == 30:
        loop_amount = 30
        print(f"{loop_amount} is the loop amount, should be 30")
        return loop_amount

    # Returns available page listings if a full page is requested
    # Returns available page listings if the requested amount is not available a non-full page
    elif uresult_amount > page_listings or remainder > page_listings:
        loop_amount = page_listings
        print(f"Page listing smaller than requested listing amount {uresult_amount} {page_listings} {remainder}")
        return loop_amount

    # Returns all remaining requested listings on a non-full page
    elif page_listings > remainder:
        loop_amount = remainder
        print("Remainder printed")
        return loop_amount

    # returns requested amount
    else:
        loop_amount = uresult_amount
        print(f"{loop_amount} is the user input, outlier")
        return loop_amount
