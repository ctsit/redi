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
@author : Mohan
email : mohan88@ufl.edu

This file tests for the function verify_and_correct_collection_date

'''
import unittest
import os
import sys
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root + 'redi/')
from lxml import etree
from redi import redi

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestVerifyAndCorrectCollectionDate(unittest.TestCase):

    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        
    def test_verify_and_correct_collection_date_case1(self):
        self.sampleData = """<study>
        <subject>
            <NAME>TestSubject1</NAME>
            <loinc_code>test1</loinc_code>
            <RESULT>0.12</RESULT>
            <DATE_TIME_STAMP>7891-11-30 11:12:00</DATE_TIME_STAMP>
            <RESULT_DATE>7891-11-30 11:12:00</RESULT_DATE>
            <STUDY_ID>1234-5678</STUDY_ID>
        </subject>
        <subject>
            <NAME>TestSubject2</NAME>
            <loinc_code>test2</loinc_code>
            <RESULT>8.7</RESULT>
            <DATE_TIME_STAMP></DATE_TIME_STAMP>
            <RESULT_DATE>1909-08-27 16:13:00</RESULT_DATE>
            <STUDY_ID>987-654</STUDY_ID>
        </subject>
    </study>
"""
        self.sampleData_tree= etree.ElementTree(etree.fromstring(self.sampleData))

        self.result = """<study>
        <subject>
            <NAME>TestSubject1</NAME>
            <loinc_code>test1</loinc_code>
            <RESULT>0.12</RESULT>
            <DATE_TIME_STAMP>7891-11-30 11:12:00</DATE_TIME_STAMP>
            <STUDY_ID>1234-5678</STUDY_ID>
        </subject>
        <subject>
            <NAME>TestSubject2</NAME>
            <loinc_code>test2</loinc_code>
            <RESULT>8.7</RESULT>
            <DATE_TIME_STAMP>1909-08-23 16:13:00</DATE_TIME_STAMP>
            <STUDY_ID>987-654</STUDY_ID>
        </subject>
    </study>
"""
        input_date_format = '%Y-%m-%d %H:%M:%S'
        result_from_method = redi.verify_and_correct_collection_date(self.sampleData_tree, input_date_format)
        result_str = etree.tostring(result_from_method[0], method='xml', pretty_print=True)
        self.assertEqual(self.result, result_str)

    def test_verify_and_correct_collection_date_case2(self):
        self.sampleData = """<study>
        <subject>
            <NAME>TestSubject1</NAME>
            <loinc_code>test1</loinc_code>
            <RESULT>0.12</RESULT>
            <RESULT_DATE>7891-11-30 11:12:00</RESULT_DATE>
            <STUDY_ID>1234-5678</STUDY_ID>
        </subject>
        <subject>
            <NAME>TestSubject2</NAME>
            <loinc_code>test2</loinc_code>
            <RESULT>8.7</RESULT>
            <STUDY_ID>987-654</STUDY_ID>
        </subject>
    </study>
"""
        self.sampleData_tree= etree.ElementTree(etree.fromstring(self.sampleData))

        self.result = """<study>
        <subject>
            <NAME>TestSubject1</NAME>
            <loinc_code>test1</loinc_code>
            <RESULT>0.12</RESULT>
            <DATE_TIME_STAMP>7891-11-26 11:12:00</DATE_TIME_STAMP><STUDY_ID>1234-5678</STUDY_ID>
        </subject>
        <subject>
            <NAME>TestSubject2</NAME>
            <loinc_code>test2</loinc_code>
            <RESULT>8.7</RESULT>
            <STUDY_ID>987-654</STUDY_ID>
        </subject>
    </study>
"""
        input_date_format = '%Y-%m-%d %H:%M:%S'
        result_from_method = redi.verify_and_correct_collection_date(self.sampleData_tree, input_date_format)
        result_str = etree.tostring(result_from_method[0], method='xml', pretty_print=True)
        self.assertEqual(self.result, result_str)

    def test_verify_and_correct_collection_date_case3(self):
        # for date_time_stamp falling in february of a non leap year
        self.sampleData = """<study>
        <subject>
            <NAME>TestSubject1</NAME>
            <loinc_code>test1</loinc_code>
            <RESULT>0.12</RESULT>
            <DATE_TIME_STAMP>7891-11-30 11:12:00</DATE_TIME_STAMP>
            <RESULT_DATE>7891-11-30 11:12:00</RESULT_DATE>
            <STUDY_ID>1234-5678</STUDY_ID>
        </subject>
        <subject>
            <NAME>TestSubject2</NAME>
            <loinc_code>test2</loinc_code>
            <RESULT>8.7</RESULT>
            <DATE_TIME_STAMP></DATE_TIME_STAMP>
            <RESULT_DATE>1909-03-01 16:13:00</RESULT_DATE>
            <STUDY_ID>987-654</STUDY_ID>
        </subject>
    </study>
"""
        self.sampleData_tree= etree.ElementTree(etree.fromstring(self.sampleData))

        self.result = """<study>
        <subject>
            <NAME>TestSubject1</NAME>
            <loinc_code>test1</loinc_code>
            <RESULT>0.12</RESULT>
            <DATE_TIME_STAMP>7891-11-30 11:12:00</DATE_TIME_STAMP>
            <STUDY_ID>1234-5678</STUDY_ID>
        </subject>
        <subject>
            <NAME>TestSubject2</NAME>
            <loinc_code>test2</loinc_code>
            <RESULT>8.7</RESULT>
            <DATE_TIME_STAMP>1909-02-25 16:13:00</DATE_TIME_STAMP>
            <STUDY_ID>987-654</STUDY_ID>
        </subject>
    </study>
"""
        input_date_format = '%Y-%m-%d %H:%M:%S'
        result_from_method = redi.verify_and_correct_collection_date(self.sampleData_tree, input_date_format)
        result_str = etree.tostring(result_from_method[0], method='xml', pretty_print=True)
        self.assertEqual(self.result, result_str)
        
    def test_verify_and_correct_collection_date_case4(self):
        # for date_time_stamp falling in february of a leap year
        self.sampleData = """<study>
        <subject>
            <NAME>TestSubject1</NAME>
            <loinc_code>test1</loinc_code>
            <RESULT>0.12</RESULT>
            <RESULT_DATE>8000-03-01 11:12:00</RESULT_DATE>
            <STUDY_ID>1234-5678</STUDY_ID>
        </subject>
        <subject>
            <NAME>TestSubject2</NAME>
            <loinc_code>test2</loinc_code>
            <RESULT>8.7</RESULT>
            <STUDY_ID>987-654</STUDY_ID>
        </subject>
    </study>
"""
        self.sampleData_tree= etree.ElementTree(etree.fromstring(self.sampleData))

        self.result = """<study>
        <subject>
            <NAME>TestSubject1</NAME>
            <loinc_code>test1</loinc_code>
            <RESULT>0.12</RESULT>
            <DATE_TIME_STAMP>8000-02-26 11:12:00</DATE_TIME_STAMP><STUDY_ID>1234-5678</STUDY_ID>
        </subject>
        <subject>
            <NAME>TestSubject2</NAME>
            <loinc_code>test2</loinc_code>
            <RESULT>8.7</RESULT>
            <STUDY_ID>987-654</STUDY_ID>
        </subject>
    </study>
"""
        input_date_format = '%Y-%m-%d %H:%M:%S'
        result_from_method = redi.verify_and_correct_collection_date(self.sampleData_tree, input_date_format)
        result_str = etree.tostring(result_from_method[0], method='xml', pretty_print=True)
        self.assertEqual(self.result, result_str)

    def test_verify_and_correct_collection_date_case5(self):
        self.sampleData = """<study>
        <subject>
            <NAME>TestSubject1</NAME>
            <loinc_code>test1</loinc_code>
            <RESULT>0.12</RESULT>
            <STUDY_ID>1234-5678</STUDY_ID>
        </subject>
    </study>
"""
        self.sampleData_tree= etree.ElementTree(etree.fromstring(self.sampleData))

        self.result = """<study>
        <subject>
            <NAME>TestSubject1</NAME>
            <loinc_code>test1</loinc_code>
            <RESULT>0.12</RESULT>
            <STUDY_ID>1234-5678</STUDY_ID>
        </subject>
    </study>
"""
        input_date_format = '%Y-%m-%d %H:%M:%S'
        result_from_method = redi.verify_and_correct_collection_date(self.sampleData_tree, input_date_format)
        result_str = etree.tostring(result_from_method[0], method='xml', pretty_print=True)
        self.assertEqual(self.result, result_str)

    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
