"""
Verifies the functionality of bin.redi.SentEventIndex
"""
import unittest

from bin import redi


class TestSentEventIndex(unittest.TestCase):

    def test_len(self):
        index = redi.SentEventIndex("", writer=lambda o, f: None,
                                    reader=lambda f: [])
        self.assertEqual(0, len(index))

        index.mark_sent("007", "new_hire", "1_arm_1")
        index.mark_sent("007", "new_hire", "2_arm_1")

        self.assertEqual(2, len(index))

    def test_was_sent(self):
        index = redi.SentEventIndex("", writer=lambda o, f: None,
                                    reader=lambda f: [])

        index.mark_sent("007", "new_hire", "1_arm_1")

        self.assertTrue(index.was_sent("007", "new_hire", "1_arm_1"))

    def test_mark_sent(self):
        self.__tally = 0

        index = redi.SentEventIndex("", self.__dummy_writer,
                                    reader=lambda f: [])
        index.mark_sent("007", "new_hire", "1_arm_1")
        index.mark_sent("007", "new_hire", "2_arm_1")

        self.assertEqual(2, self.__tally)

    def __dummy_writer(self, obj, filename):
        self.__tally += 1


if __name__ == "__main__":
    unittest.main()
