import unittest
import redi

class TestArgs(unittest.TestCase):
    """ Verify that the command line arguments are parsed properly"""

    def test_parse_args(self):
        """Check boolean arguments parsing"""

        # Verify that not passing `resume` sets it to false
        args = redi.parse_args('--verbose --dryrun'.split())
        self.assertTrue(args['verbose'])
        self.assertTrue(args['dryrun'])
        self.assertFalse(args['resume'])
        self.assertFalse(args['keep'])
        self.assertFalse(args['emrdata'])

        # Verify that order does not matter
        args = redi.parse_args('--resume --verbose --dryrun'.split())
        self.assertTrue(args['resume'])
        self.assertTrue(args['verbose'])
        self.assertTrue(args['dryrun'])
        self.assertFalse(args['keep'])
        self.assertFalse(args['emrdata'])

        args = redi.parse_args('--verbose --resume --dryrun'.split())
        self.assertTrue(args['verbose'])
        self.assertTrue(args['resume'])
        self.assertTrue(args['dryrun'])
        self.assertFalse(args['keep'])
        self.assertFalse(args['emrdata'])

        # Verify that `keep` and `emrdata` args are read properly
        args = redi.parse_args('--verbose -e -k'.split())
        self.assertTrue(args['verbose'])
        self.assertTrue(args['emrdata'])
        self.assertTrue(args['keep'])
        self.assertFalse(args['resume'])
        self.assertFalse(args['dryrun'])

if __name__ == '__main__':
    unittest.main()
