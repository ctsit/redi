import unittest
import datetime
from datetime import timedelta
from redi import redi_lib


class TestDaysSinceToday(unittest.TestCase):

    """
    Verify the difference from a past date
    Verify the difference from a future date
    """
    def test(self):
        past10 = datetime.datetime.now() - timedelta(days = 10)
        future11 = datetime.datetime.now() + timedelta(days = 11)

        diff_past = redi_lib.get_days_since_today( str(past10.strftime('%Y-%m-%d %H:%M:%S') ) )
        self.assertEqual(10, diff_past)

        diff_future = redi_lib.get_days_since_today( str(future11.strftime('%Y-%m-%d %H:%M:%S') ) )
        self.assertEqual(-11, diff_future)


if __name__ == "__main__":
    unittest.main()
