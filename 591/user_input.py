import datetime


# from datetime import datetime


# User enters number
def get_user_input(s: str):
    return str(input(s))


# Check valid number entry for listing request


def parse_listing_total(s: str) -> int:
    if s == "":
        raise Exception("Please enter Integer between 0 and 101")

    if not (s.isnumeric() and 0 <= int(s) < 101):
        raise Exception("Please only enter Integers between 0 and 101")

    return int(s)


# Check valid number entry for hours from


def parse_date_start_search(s: str) -> datetime:
    if s == "":
        raise Exception("Please enter Integer between 0 and 121")

    if not (s.isnumeric() and 0 <= int(s) < 121):
        raise Exception("Please only enter Integers between 0 and 121")

    return datetime.datetime.now() - (datetime.timedelta(0, 0, 0, 0, 0, int(s)))


# demonstration on how to repeat user input
# if __name__ == '__main__':
#     while True:
#         try:
#             hours = parse_user_input_hours(get_user_input("Enter number of hours you want to search back from:"))
#         except Exception as e:
#             print(e)
#         try:
#             listings = parse_result_hours(get_user_input("Enter number of listings you want to filter through:"))
#         except Exception as e:
#             print(e)


# print(parse_result_hours())
