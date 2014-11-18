"""
Utility module for throttling calls to a function
"""

import collections
import datetime
import time

__author__ = "University of Florida CTS-IT Team"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause"


class Throttle(object):
    """
    Limits the number of calls to a function to a given rate.

    The rate limit is equal to the max_calls over the interval_in_seconds.

    :param function: function to call after throttling
    :param max_calls: maximum number of calls allowed
    :param interval_in_seconds: size of the sliding window
    """
    def __init__(self, function, max_calls, interval_in_seconds=60):
        assert max_calls > 0
        assert interval_in_seconds > 0

        self._actual = function
        self._max_requests = max_calls
        self._interval = datetime.timedelta(seconds=interval_in_seconds)
        self._timestamps = collections.deque(maxlen=self._max_requests)

    def __call__(self, *args, **kwargs):
        """ Conditionally delays before calling the function """
        self._wait()
        self._actual(*args, **kwargs)

    def _limit_reached(self):
        """ Returns True if the maximum number of calls has been reached """
        return len(self._timestamps) == self._max_requests

    @staticmethod
    def _now():
        # Used during unit testing
        return datetime.datetime.now()

    @staticmethod
    def _sleep(seconds):
        # Used during unit testing
        return time.sleep(seconds)

    def _wait(self):
        """ Sleeps for the remaining interval if the limit has been reached """
        now = self._now()

        limit_reached = len(self._timestamps) == self._max_requests
        if limit_reached:
            lapsed = now - self._timestamps[0]
            if lapsed <= self._interval:
                self._sleep((self._interval - lapsed).total_seconds())
                self._timestamps.clear()

        self._timestamps.append(now)
