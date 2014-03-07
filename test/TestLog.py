'''
@author : Radha
email : rkandula@ufl.edu

This file tests the logger functionality

'''

import unittest
import os
import sys
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root+'test')
sys.path.append(proj_root+'bin')
from lxml import etree
import redi

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
        redi.configure_logging()
        #print os.path.isfile(file_name)
        # check if the file is created
        assert os.path.isfile(file_name) == True
        # remove the file created through testing
        os.remove(file_name)

if __name__ == '__main__':
    unittest.main()
