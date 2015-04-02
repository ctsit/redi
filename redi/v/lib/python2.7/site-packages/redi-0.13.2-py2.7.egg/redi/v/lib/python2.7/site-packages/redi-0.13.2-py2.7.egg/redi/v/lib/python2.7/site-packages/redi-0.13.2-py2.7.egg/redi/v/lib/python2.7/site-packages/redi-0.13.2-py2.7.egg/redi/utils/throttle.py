# Contributors:
# Christopher P. Barnes <senrabc@gmail.com>
# Andrei Sura: github.com/indera
# Mohan Das Katragadda <mohan.das142@gmail.com>
# Philip Chase <philipbchase@gmail.com>
# Ruchi Vivek Desai <ruchivdesai@gmail.com>
# Taeber Rapczak <taeber@ufl.edu>
# Nicholas Rejack <nrejack@ufl.edu>
# Josh Hanna <josh@hanna.io>
# Copyright (c) 2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

"""
Utility module for throttling calls to a function
"""

import collections
import datetime
import logging
import time

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

    def _limit_reached(self):
        """ Returns True if the maximum number of calls has been reached """
        return len(self._timestamps) == self._max_requests

    @staticmethod
    def _now():
        # Used during unit testing
        return datetime.datetime.now()

    def _remove_old_entries(self):
        """ Removes old timestamp entries """
        # @TODO: investigate why the deque is not
        # cleared after we reach the limit

        #logger.debug("Clear the deque")
        #self._timestamps.clear()
        #return

        while (len(self._timestamps) > 0 and
               self._now() - self._timestamps[0] >= self._interval):
            self._timestamps.popleft()

    @staticmethod
    def _sleep(seconds):
        # Used during unit testing
        return time.sleep(seconds)

    def _wait(self):
        """ Sleeps for the remaining interval if the limit has been reached """
        if self._limit_reached():
            logger.warn('Throttling limit {} reached.' \
                    .format(self._max_requests))
            lapsed = self._now() - self._timestamps[0]

            if lapsed < self._interval:
                sleep_time = (self._interval - lapsed).total_seconds()
                logger.debug("Sleeping for {} seconds to prevent too many calls"
                             .format(sleep_time))
                self._sleep(sleep_time)

            self._remove_old_entries()

        self._timestamps.append(self._now())
