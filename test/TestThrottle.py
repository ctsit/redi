#!/usr/bin/env python

import datetime
import unittest

from redi.utils import throttle


class TestThrottle(unittest.TestCase):

    def test_throttle(self):
        class Clock(object):
            def __init__(self):
                self.now = datetime.datetime.now()

            def __call__(self):
                return self.now

            def add_seconds(self, seconds):
                self.now += datetime.timedelta(seconds=seconds)

        clock = Clock()
        throttle.Throttle._now = clock
        throttle.Throttle._sleep = clock.add_seconds

        call = throttle.Throttle(lambda: None, max_calls=3,
                                 interval_in_seconds=5)

        call()  # t=0
        clock.add_seconds(1)
        call()  # t=1
        clock.add_seconds(2)
        call()  # t=3
        clock.add_seconds(1)
        call()  # t=4
        self.assertEquals(1, len(call._timestamps))
        clock.add_seconds(1)
        call()  # t=5
        self.assertEquals(2, len(call._timestamps))


if __name__ == '__main__':
    unittest.main()
