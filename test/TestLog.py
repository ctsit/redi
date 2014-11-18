'''
@author : Radha
email : rkandula@ufl.edu

This file tests if the `configure_logging`
properly creates a log file

Note: the created file is destroyed at the end
'''

import unittest
import os
import sys
from redi import redi

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestLog(unittest.TestCase):

    def setUp(self):
        # initialize log file name
        self.file_name = proj_root + 'log/redi.log'

    def test_log(self):
        import os.path
        file_name = self.file_name
        sys.path.append('log')
        # remove any existing log file in log/ folder

        #if os.path.isfile(file_name):
        #    with open(file_name):
                #print "here"
        #        os.remove(file_name)
                #print os.path.isfile(file_name)

        # call the configure logging function
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)

        #print 'checking if log file was created: ' + file_name
        # check if the file is created
        assert os.path.isfile(file_name) == True

        # remove the file created through testing
        os.remove(file_name)

if __name__ == '__main__':
    unittest.main()
