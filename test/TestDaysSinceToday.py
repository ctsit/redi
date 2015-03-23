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

import unittest
import datetime
from datetime import timedelta
from redi import batch

class TestDaysSinceToday(unittest.TestCase):
    """
    Verify the difference from a past date
    Verify the difference from a future date
    """
    def test(self):
        past10 = datetime.datetime.now() - timedelta(days = 10)
        future11 = datetime.datetime.now() + timedelta(days = 11)

        diff_past = batch.get_days_since_today( str(past10.strftime('%Y-%m-%d %H:%M:%S') ) )
        self.assertEqual(10, diff_past)

        diff_future = batch.get_days_since_today( str(future11.strftime('%Y-%m-%d %H:%M:%S') ) )
        self.assertEqual(-11, diff_future)


if __name__ == "__main__":
    unittest.main()
