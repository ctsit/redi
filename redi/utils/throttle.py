"""
Utility module for throttling calls to a function
"""

import collections
import datetime
import logging
import time

__author__ = "University of Florida CTS-IT Team"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause"


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


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
        return self._actual(*args, **kwargs)

    @staticmethod
    def _now():
        # Used during unit testing
        return datetime.datetime.now()

    def _remove_old_entries(self):
        """ Removes old timestamp entries """
        while (len(self._timestamps) > 0 and
               self._now() - self._timestamps[0] >= self._interval):
            self._timestamps.popleft()

    @staticmethod
    def _sleep(seconds):
        # Used during unit testing
        return time.sleep(seconds)

    def _wait(self):
        """ Sleeps for the remaining interval if the limit has been reached """
        limit_reached = len(self._timestamps) == self._max_requests
        if limit_reached:
            logger.debug('Throttling limit reached.')
            lapsed = self._now() - self._timestamps[0]

            if lapsed < self._interval:
                sleep_time = (self._interval - lapsed).total_seconds()
                logger.debug("Sleeping for {} seconds to prevent too many calls"
                             .format(sleep_time))
                self._sleep(sleep_time)

            self._remove_old_entries()

        self._timestamps.append(self._now())
