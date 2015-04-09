#!/usr/bin/env python

# Contributors:
# Christopher P. Barnes <senrabc@gmail.com>
# Andrei Sura: github.com/indera
# Mohan Das Katragadda <mohan.das142@gmail.com>
# Philip Chase <philipbchase@gmail.com>
# Ruchi Vivek Desai <ruchivdesai@gmail.com>
# Taeber Rapczak <taeber@ufl.edu>
# Nicholas Rejack <nrejack@ufl.edu>
# Josh Hanna <josh@hanna.io>
# Copyright (c) 2014-2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

import datetime
import unittest

from redi.utils import throttle


class TestThrottle(unittest.TestCase):

    def test_throttle(self):
        clock = MockClock()
        throttle.Throttle._now = clock
        throttle.Throttle._sleep = clock.add_seconds

        call = throttle.Throttle(lambda: None, max_calls=3,
                                 interval_in_seconds=5)

        call()
        call()
        call()
        self.assertEquals(3, len(call._timestamps))
        before = clock.now

        call()

        self.assertEqual(5, (clock.now - before).total_seconds())

    def test_throttle_front_loaded(self):
        clock = MockClock()
        throttle.Throttle._now = clock
        throttle.Throttle._sleep = clock.add_seconds

        call = throttle.Throttle(lambda: None, max_calls=3,
                                 interval_in_seconds=5)

        call()
        call()
        call()
        self.assertEquals(3, len(call._timestamps))
        clock.add_seconds(5)
        before = clock.now

        call()

        self.assertEquals(1, len(call._timestamps))
        self.assertEqual(0, (clock.now - before).total_seconds())

    def test_throttle_back_loaded(self):
        clock = MockClock()
        throttle.Throttle._now = clock
        throttle.Throttle._sleep = clock.add_seconds

        call = throttle.Throttle(lambda: None, max_calls=3,
                                 interval_in_seconds=5)

        start = clock.now
        call()
        clock.add_seconds(4)
        call()
        call()
        self.assertEquals(3, len(call._timestamps))

        call()
        self.assertEquals(3, len(call._timestamps))
        self.assertEqual(5, (clock.now - start).total_seconds())

        call()
        self.assertEquals(2, len(call._timestamps))
        self.assertEqual(9, (clock.now - start).total_seconds())


class MockClock(object):
    def __init__(self):
        self.now = datetime.datetime.now()

    def __call__(self):
        return self.now

    def add_seconds(self, seconds):
        self.now += datetime.timedelta(seconds=seconds)


if __name__ == '__main__':
    unittest.main()
