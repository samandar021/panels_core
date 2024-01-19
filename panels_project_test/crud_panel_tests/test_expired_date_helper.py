import unittest
from datetime import datetime

from modules.helper.expired_date_helper import calculate_expired_date


class TestCalculateExpiredDate(unittest.TestCase):
    def test_first_of_month(self):
        self.assertEqual(
            datetime.fromtimestamp(calculate_expired_date(datetime(2023, 1, 1))),
            datetime(2023, 2, 1)
        )

    def test_end_of_month(self):
        self.assertEqual(
            datetime.fromtimestamp(calculate_expired_date(datetime(2023, 1, 31))),
            datetime(2023, 3, 1)
        )

    def test_middle_of_month(self):
        self.assertEqual(
            datetime.fromtimestamp(calculate_expired_date(datetime(2023, 1, 15))),
            datetime(2023, 2, 15)
        )

    def test_leap_year(self):
        self.assertEqual(
            datetime.fromtimestamp(calculate_expired_date(datetime(2024, 2, 29))),
            datetime(2024, 4, 1)
        )

    def test_non_leap_year(self):
        self.assertEqual(
            datetime.fromtimestamp(calculate_expired_date(datetime(2023, 2, 28))),
            datetime(2023, 3, 28)
        )

    def test_december(self):
        self.assertEqual(
            datetime.fromtimestamp(calculate_expired_date(datetime(2023, 12, 31))),
            datetime(2024, 2, 1)
        )
