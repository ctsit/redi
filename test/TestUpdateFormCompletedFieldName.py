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

import unittest
import os
from lxml import etree
from redi import redi

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'


class TestUpdateFormCompletedFieldName(unittest.TestCase):

    def setUp(self):
        self.raw_xml = """<?xml version='1.0' encoding='US-ASCII'?>
<study>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>11/20/17</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp/><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>11/20/17</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>10/25/20</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp/><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/></subject>
</study>
"""
        self.data_tree = etree.ElementTree(etree.fromstring(self.raw_xml))

        self.form_events = """<?xml version='1.0' encoding='US-ASCII'?>
<redcapProject>
	<name>My Test Project</name>
	<form>
		<name>cbc</name>
		<formDateField>cbc_lbdtc</formDateField>
		<formCompletedFieldName>cbc_complete</formCompletedFieldName>
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
		<formDateField>chemistry_lbdtc</formDateField>
		<formCompletedFieldName>chemistry_complete</formCompletedFieldName>
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

        self.output = """<?xml version='1.0' encoding='US-ASCII'?>
<study>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>11/20/17</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp/><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName>undefined</formCompletedFieldName></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>11/20/17</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName>cbc_complete</formCompletedFieldName></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>10/25/20</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp/><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName>chemistry_complete</formCompletedFieldName></subject>
</study>
"""
        self.expect = etree.tostring(etree.fromstring(self.output))
        return()


    def test_update_form_completed_field_name(self):
        redi.update_formcompletedfieldname(self.data_tree, self.form_events_tree, 'undefined')
        self.result = etree.tostring(self.data_tree)
        self.assertEqual(self.expect, self.result)

    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
