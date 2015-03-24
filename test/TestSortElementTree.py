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


class TestSortElementTree(unittest.TestCase):

    def setUp(self):
        # un-sorted XML file
        self.unsorted = """
        <study>
        <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1903-03-31 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1903-03-31 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>12/12/16</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <loinc_code>1577876</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1907-09-10 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1903-03-31 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1903-03-31 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>12/12/16</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <loinc_code>1577876</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1907-09-10 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    </study>"""

        # above data manually sorted
        self.sorted = """
<study>
        <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>12/12/16</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <loinc_code>1577876</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1907-09-10 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1903-03-31 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1903-03-31 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>12/12/16</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <loinc_code>1577876</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1907-09-10 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1903-03-31 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1903-03-31 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    </study>"""

    def test_sort_elementtree(self):
        self.data = etree.ElementTree(etree.fromstring(self.unsorted))
        redi.sort_element_tree(self.data)
        result = etree.tostring(self.data)
        self.expect = etree.tostring(etree.fromstring(self.sorted))
        self.assertEqual(self.expect, result)

if __name__ == '__main__':
    unittest.main()

