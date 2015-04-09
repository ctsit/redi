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

This file tests for the function update_formdatefield and checks if the
formDateField of the resulting element tree is filled or not

'''
import unittest
import os
from lxml import etree
from redi import redi

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestUpdateFormDateField(unittest.TestCase):

    def setUp(self):
        self.sortedData = """
    <study>
    <subject>
        <Study_Id>001-0001</Study_Id>
        <Study_Start>05/08/21</Study_Start>
        <Collection_Date>09/19/17</Collection_Date>
        <Collection_Time>11:57</Collection_Time>
        <Qualifying_Result>Y</Qualifying_Result>
        <Study_Stop>12/17/16</Study_Stop>
        <Component_Name>ALBUMIN</Component_Name>
        <loinc_code>1810650</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Reference_Low>3.5</Reference_Low>
        <Reference_High>5.0</Reference_High>
        <Result_Value>3.9</Result_Value>
    <timestamp>1904-10-28</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><formImportedFieldName/><redcapFieldNameValue/><redcapFieldNameUnits/></subject>
    <subject>
        <Study_Id>001-0001</Study_Id>
        <Study_Start>05/08/21</Study_Start>
        <Collection_Date>09/19/17</Collection_Date>
        <Collection_Time>11:57</Collection_Time>
        <Qualifying_Result>Y</Qualifying_Result>
        <Study_Stop>12/17/16</Study_Stop>
        <Component_Name>ALKALINE PHOSPHATASE</Component_Name>
        <loinc_code>1525848</loinc_code>
        <Reference_Unit>U/L</Reference_Unit>
        <Reference_Low>35</Reference_Low>
        <Reference_High>129</Reference_High>
        <Result_Value>112</Result_Value>
    <timestamp>1904-10-28</timestamp><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><formImportedFieldName/><redcapFieldNameValue/><redcapFieldNameUnits/></subject>
    <subject>
        <Study_Id>001-0001</Study_Id>
        <Study_Start>05/08/21</Study_Start>
        <Collection_Date>09/19/17</Collection_Date>
        <Collection_Time>11:57</Collection_Time>
        <Qualifying_Result>Y</Qualifying_Result>
        <Study_Stop>12/17/16</Study_Stop>
        <Component_Name>ALPHA FETO PROT</Component_Name>
        <loinc_code>683</loinc_code>
        <Reference_Unit>ng/mL</Reference_Unit>
        <Reference_Low>0.0</Reference_Low>
        <Reference_High>8.7</Reference_High>
        <Result_Value>3.0</Result_Value>
    <timestamp>1904-10-28</timestamp><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><formImportedFieldName/><redcapFieldNameValue/><redcapFieldNameUnits/></subject>
    </study>"""

        self.data = etree.ElementTree(etree.fromstring(self.sortedData))

        self.form_events = """<?xml version="1.0" encoding="UTF-8"?>
<redcapProject>
    <name>My Project</name>
    <form>
        <name>cbc</name>
        <formDateField>cbc_lbdtc</formDateField>
        <formCompletedFieldName>cbc_complete</formCompletedFieldName>
        <formImportedFieldName>cbc_nximport</formImportedFieldName>
        <event>
            <name>1_arm_1</name>
        </event>
        <event>
            <name>2_arm_1</name>
        </event>
        <event>
            <name>3_arm_1</name>
        </event>
    </form>
    <form>
        <name>chemistry</name>
        <formDateField>chem_lbdtc</formDateField>
        <formCompletedFieldName>chemistry_complete</formCompletedFieldName>
        <formImportedFieldName>chem_nximport</formImportedFieldName>
        <event>
            <name>1_arm_1</name>
        </event>
        <event>
            <name>2_arm_1</name>
        </event>
        <event>
            <name>3_arm_1</name>
        </event>
    </form>
</redcapProject>

"""

        self.form_events_tree = etree.ElementTree(etree.fromstring(self.form_events))

    def test_update_formdatefield(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        redi.update_formdatefield(self.data, self.form_events_tree)

	    # output raw file to check it
        #redi.write_element_tree_to_file(self.data, 'rawData.xml')

        # initialize a dictionary for the formdatefield
        # [key, value] = [formdatefield, filled or not?(0/1)]
        isFormDateFieldFilled = {}
        for subject in self.data.iter('subject'):
            form_date_field = subject.find('formDateField').text
            if not form_date_field:
                isFormDateFieldFilled[form_date_field] = 1
        status=1
        for key,value in isFormDateFieldFilled.items():
            if value != status:
                status = 0
                break
        self.assertEqual(status,1)

    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
