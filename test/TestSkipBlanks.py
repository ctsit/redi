import unittest


class TestSkipBlanks(unittest.TestCase):
    def test_switch(self):
        import bin.redi
        redi = reload(bin.redi)

        args = redi.parse_args('--verbose --skip-blanks'.split())
        self.assertTrue(args['skip_blanks'])

        args = redi.parse_args('--verbose'.split())
        self.assertFalse(args['skip_blanks'])


if __name__ == '__main__':
    unittest.main()
