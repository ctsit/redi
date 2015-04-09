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

"""
Verifies the functionality of bin.redi.SentEventIndex
"""
import unittest

from redi import redi


class TestSentEventIndex(unittest.TestCase):

    def test_len(self):
        index = redi.SentEvents("", writer=lambda o, f: None,
                                    reader=lambda f: [])
        self.assertEqual(0, len(index))

        index.mark_sent("007", "new_hire", "1_arm_1")
        index.mark_sent("007", "new_hire", "2_arm_1")

        self.assertEqual(2, len(index))

    def test_was_sent(self):
        index = redi.SentEvents("", writer=lambda o, f: None,
                                    reader=lambda f: [])

        index.mark_sent("007", "new_hire", "1_arm_1")

        self.assertTrue(index.was_sent("007", "new_hire", "1_arm_1"))

    def test_mark_sent(self):
        self.__tally = 0

        index = redi.SentEvents("", self.__dummy_writer,
                                    reader=lambda f: [])
        index.mark_sent("007", "new_hire", "1_arm_1")
        index.mark_sent("007", "new_hire", "2_arm_1")

        self.assertEqual(2, self.__tally)

    def __dummy_writer(self, obj, filename):
        self.__tally += 1


if __name__ == "__main__":
    unittest.main()
