import unittest
import sys
import os
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root + 'bin/')
from lxml import etree
import redi

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
        <Component_ID>1534436</Component_ID>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1903-03-31 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <Component_ID>1534435</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1903-03-31 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>12/12/16</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <Component_ID>1577876</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1907-09-10 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1903-03-31 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <Component_ID>1534436</Component_ID>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <Component_ID>1534435</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1903-03-31 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>12/12/16</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <Component_ID>1577876</Component_ID>
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
        <Component_ID>1577876</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1907-09-10 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <Component_ID>1534435</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1903-03-31 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1903-03-31 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>11</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <Component_ID>1534436</Component_ID>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>12/12/16</Collection_Date>
        <Collection_Time>11:00</Collection_Time>
        <Component_Name>WHITE BLOOD CELL COUNT</Component_Name>
        <Component_ID>1577876</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>8.7</Result_Value>
    <timestamp>1907-09-10 11:00</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <Component_ID>1534435</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp>1907-09-24 13:50</timestamp><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp>1903-03-31 12:38</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>11/30/16</Collection_Date>
        <Collection_Time>16:01</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.9</Result_Value>
    <timestamp>1903-03-31 16:01</timestamp><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/><timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <STUDY_ID>22</STUDY_ID>
        <Collection_Date>06/09/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <Component_ID>1534436</Component_ID>
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

