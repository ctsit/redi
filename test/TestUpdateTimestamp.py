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

'''
@author : Radha
email : rkandula@ufl.edu

This file tests for the function updateTimeStamp.
we call the function and check if the function updates the timestamps of all the subjects
if all the subject's timestamps are updated the status value stays 1
else the status value is flipped to 0 and loop is exited and Hence the test fails in
assertion

'''
import unittest
import os
from lxml import etree
from redi import redi

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestUpdateTimestamp(unittest.TestCase):

    def setUp(self):
        # initialize the data with element tree
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        self.test_xml = """<?xml version="1.0" encoding="utf8"?>
<study>
    <subject>
        <NAME>TSH REFLEX</NAME>
        <loinc_code>1552152</loinc_code>
        <RESULT>0.74</RESULT>
        <REFERENCE_LOW>0.27</REFERENCE_LOW>
        <REFERENCE_HIGH>4.20</REFERENCE_HIGH>
        <REFERENCE_UNIT>mIU/L</REFERENCE_UNIT>
        <DATE_TIME_STAMP>1903-11-27 15:13:00</DATE_TIME_STAMP>
        <STUDY_ID>59</STUDY_ID>
    </subject>
    <subject>
        <NAME>HEP C RNA, QUANT REAL-TIME</NAME>
        <loinc_code>740</loinc_code>
        <RESULT>5.8</RESULT>
        <REFERENCE_LOW></REFERENCE_LOW>
        <REFERENCE_HIGH></REFERENCE_HIGH>
        <REFERENCE_UNIT>log IU</REFERENCE_UNIT>
        <DATE_TIME_STAMP>1903-11-27 15:13:00</DATE_TIME_STAMP>
        <STUDY_ID>59</STUDY_ID>
    </subject>
    <subject>
        <NAME>HCV QUANTITATIVE INTERPRETATION</NAME>
        <loinc_code>1534483</loinc_code>
        <RESULT>Detected</RESULT>
        <REFERENCE_LOW></REFERENCE_LOW>
        <REFERENCE_HIGH></REFERENCE_HIGH>
        <REFERENCE_UNIT></REFERENCE_UNIT>
        <DATE_TIME_STAMP>1903-11-27 15:13:00</DATE_TIME_STAMP>
        <STUDY_ID>59</STUDY_ID>
    </subject>
    </study>"""
        self.data = etree.ElementTree(etree.fromstring(self.test_xml))
        self.input_date_format = "%Y-%m-%d %H:%M:%S"
        self.output_date_format = "%Y-%m-%d"

    def test_updateTimeStamp(self):
	    # add blank elements to each subject in data tree
        redi.add_elements_to_tree(self.data)

        # function to be tested
        redi.update_time_stamp(self.data, self.input_date_format, self.output_date_format)

	    # output raw file to check it
        #redi.write_element_tree_to_file(self.data, 'rawData.xml')

        #initialize a dictionary for the timestamps
        # key,value = timestamp, filled or not?(0/1)
        isStampFilled = {}
        for subject in self.data.iter('subject'):
            ts = subject.find('timestamp').text
            if not ts:
                isStampFilled[ts] = 1
        status=1
        for key,value in isStampFilled.items():
            if value != status:
                status = 0
                break
        self.assertEqual(status,1)
    
    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
