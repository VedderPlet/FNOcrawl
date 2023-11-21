import datetime
import unittest

from loop_listings import set_loop_amount
from date_data import string_to_datetime
from user_input import parse_date_start_search, parse_listing_total


class TestScrapePage(unittest.TestCase):
    def test_multiple_pages(self):
        pass

    def test_whole_page(self):
        pass

    def test_partial_page(self):
        pass



class TestUserInput(unittest.TestCase):
    def test_hour_no_input(self):
        with self.assertRaises(Exception):
            parse_date_start_search("")

    def test_hour_out_of_bounds(self):
        with self.assertRaises(Exception):
            parse_date_start_search("800")

    def test_hour_not_a_number(self):
        with self.assertRaises(Exception):
            parse_date_start_search("cake")

    def test_valid_date(self):
        expected_value = datetime.datetime.now() - datetime.timedelta(0, 0, 0, 0, 0, 1)
        predicted_value = parse_date_start_search("1")
        self.assertEqual(expected_value.year, predicted_value.year)
        self.assertEqual(expected_value.month, predicted_value.month)
        self.assertEqual(expected_value.day, predicted_value.day)
        self.assertEqual(expected_value.hour, predicted_value.hour)
        self.assertEqual(expected_value.minute, predicted_value.minute)

    def test_listing_no_input(self):
        with self.assertRaises(Exception):
            parse_listing_total("")

    def test_valid_listing(self):
        self.assertEqual(parse_listing_total("5"), 5)

    def test_listing_out_of_bounds(self):
        with self.assertRaises(Exception):
            parse_listing_total("300")

    def test_listing_not_a_number(self):
        with self.assertRaises(Exception):
            parse_listing_total("cake")


class TestListingLoops(unittest.TestCase):

    # Prints 1 full page of available listings [Full Page]
    def test_get_full_page(self):
        self.assertEqual(set_loop_amount(50, 1, 30, 0), 30)

    # Prints available listings when a full page is requested [Partial Page]
    # Prints available listings on the last non-full page when requested amount is too much
    def test_available_listings(self):
        self.assertEqual(set_loop_amount(80, 1, 5, 0), 5)
        self.assertEqual(set_loop_amount(25, 0, 6, 9), 6)

    # Prints remaining requested listings (last non-full page) when there are too many listings
    def test_remaining_listings(self):
        self.assertEqual(set_loop_amount(0, 0, 30, 5), 5)

    # Prints the amount requested if there are enough listings
    def test_requested_listings_under_30(self):
        self.assertEqual(set_loop_amount(4, 0, 9, 4), 4)

    def test_random_configuration(self):
        self.assertEqual(set_loop_amount(4, 0, 30, 4), 4)


class TestParseString(unittest.TestCase):

    # just now valid
    def test_valid_just_now(self):
        just_now_text = "此房屋在剛剛發佈"
        fifty_nine_seconds_ago = string_to_datetime(just_now_text)
        expected_value = datetime.datetime.now() - (datetime.timedelta(0,
                                                                       59, 0, 0,
                                                                       0, 0, 0))
        self.assertEqual(fifty_nine_seconds_ago.strftime("%S"), expected_value.strftime("%S"))

    # month and day valid
    def test_valid_month_and_day(self):
        month_day_text = "此房屋在2月3日發佈(3小時內更新)"
        calendar_date = string_to_datetime(month_day_text)
        expected_date = datetime.datetime(int(datetime.datetime.now().strftime("%Y")), 2, 3)
        self.assertEqual(calendar_date.strftime("%x"), expected_date.strftime("%x"))

    # Days ago valid
    def test_valid_days_ago(self):
        days_ago_text = "此房屋在1天前發佈(20小時內更新)"
        days_ago = string_to_datetime(days_ago_text)
        expected_value = datetime.datetime.now() - (datetime.timedelta(1,
                                                                       0, 0, 0,
                                                                       0, 0, 0))
        self.assertEqual(expected_value.strftime("%d"), days_ago.strftime("%d"))

    # hours ago valid
    def test_valid_hours_ago(self):
        hours_ago_text = "此房屋在1小時前發佈"
        hours_ago = string_to_datetime(hours_ago_text)
        expected_value = datetime.datetime.now() - (datetime.timedelta(0,
                                                                       0, 0, 0,
                                                                       0, 1, 0))
        self.assertEqual(expected_value.strftime("%H"), hours_ago.strftime("%H"))
        hours_ago_text = "此房屋在23小時前發佈\n(15小時內更新)"
        hours_ago = string_to_datetime(hours_ago_text)
        # 2023-03-02 09:09:25
        expected_value = datetime.datetime(2023, 3, 2, 9, 9, 25)
        print(hours_ago)
        self.assertFalse(expected_value <= hours_ago)

    # minutes ago valid
    def test_valid_minutes_ago(self):
        minute_ago_text = "此房屋在45分鐘前發佈"
        minutes_ago = string_to_datetime(minute_ago_text)
        expected_value = datetime.datetime.now() - (datetime.timedelta(0,
                                                                       0, 0, 0,
                                                                       45, 0, 0))
        self.assertEqual(expected_value.strftime("%M"), minutes_ago.strftime("%M"))

    # no string to parse
    def test_no_string_parse(self):
        with self.assertRaises(Exception):
            invalid_date_string = "abcdefghijklmnopqrstuvwxyxz"
            string_to_datetime(invalid_date_string)


if __name__ == '__main__':
    unittest.main()
