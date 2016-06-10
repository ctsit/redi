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
import mock
from lxml import etree
import os
from redi import redi

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestUpdateEventName_KeepAllEvents(unittest.TestCase):

    def setUp(self):
        redi.keep_all_results = True
        self.sortedData = """
    <study>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>07/29/17</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <loinc_code>1577876</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1906-03-15 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>07/29/17</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1906-03-15 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>05/20/20</Collection_Date>
        <Collection_Time>12:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <loinc_code>1577876</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1903-04-16 12:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>05/20/20</Collection_Date>
        <Collection_Time>12:00</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1903-04-16 12:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
        <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>10/12/18</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1908-07-01 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
        <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>10/12/18</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1908-07-01 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>05/20/20</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp>1903-04-16 13:50</timestamp><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>07/29/17</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <loinc_code>1577876</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1906-03-15 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>05/20/20</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1903-04-16 13:50</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>10/12/18</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1908-07-01 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>10/12/18</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1908-07-01 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>05/20/20</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp>1903-04-16 13:50</timestamp><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    </study>"""

        self.data = etree.ElementTree(etree.fromstring(self.sortedData))

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
		<event>
			<name>4_arm_1</name>
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
		<event>
			<name>4_arm_1</name>
		</event>
    </form>
</redcapProject>
"""

        self.form_events_tree = etree.ElementTree(etree.fromstring(self.form_events))

        self.output = """<study>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>07/29/17</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <loinc_code>1577876</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1906-03-15 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName>1_arm_1</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>07/29/17</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1906-03-15 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName>2_arm_1</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>05/20/20</Collection_Date>
        <Collection_Time>12:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <loinc_code>1577876</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1903-04-16 12:00</timestamp><redcapFormName>cbc</redcapFormName><eventName>3_arm_1</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>05/20/20</Collection_Date>
        <Collection_Time>12:00</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1903-04-16 12:00</timestamp><redcapFormName>cbc</redcapFormName><eventName>4_arm_1</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
        <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>10/12/18</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1908-07-01 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName>1_arm_1</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
        <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>10/12/18</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1908-07-01 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName>2_arm_1</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>05/20/20</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp>1903-04-16 13:50</timestamp><redcapFormName>undefined</redcapFormName><eventName>undefined</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>07/29/17</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <loinc_code>1577876</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1906-03-15 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName>1_arm_1</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>05/20/20</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1903-04-16 13:50</timestamp><redcapFormName>cbc</redcapFormName><eventName>2_arm_1</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>10/12/18</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1908-07-01 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName>1_arm_1</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>10/12/18</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1908-07-01 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName>2_arm_1</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>05/20/20</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp>1903-04-16 13:50</timestamp><redcapFormName>undefined</redcapFormName><eventName>undefined</eventName><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    </study>"""

        self.expect = etree.tostring(etree.fromstring(self.output))

    def test_update_event_name_keep_all_events(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        redi.update_event_name(self.data, self.form_events_tree, 'undefined')
        result = etree.tostring(self.data)
        self.assertEqual(self.expect, result)

    def tearDown(self):
        return()

if __name__ == "__main__":
    unittest.main()
