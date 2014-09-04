"""Tests support for skipping blank events when sending RedCAP data"""

import unittest


class TestSkipBlanks(unittest.TestCase):
    """Tests support for skipping blank events when sending RedCAP data"""
    # pylint: disable=R0904

    def test_switch(self):
        """Test to check --skip-blanks and document its usage"""
        # pylint: disable=W0622
        import bin.redi
        redi = reload(bin.redi)

        args = redi.parse_args('--verbose --skip-blanks'.split())
        self.assertTrue(args['skip_blanks'])

        args = redi.parse_args('--verbose'.split())
        self.assertFalse(args['skip_blanks'])


if __name__ == '__main__':
    unittest.main()
