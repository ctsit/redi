import json
import unittest
import tempfile
import os
import sys

from lxml import etree

sys.path.append('bin/')
import redi

class TestAddElementsToTree(unittest.TestCase):

    def setUp(self):
        self.raw_xml = """<?xml version='1.0' encoding='US-ASCII'?>
<study>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>12/01/20</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <Component_ID>1534436</Component_ID>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
</subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>12/01/20</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <Component_ID>1534435</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
</subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>04/18/19</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
</subject>
</study>
"""
        self.data_tree = etree.ElementTree(etree.fromstring(self.raw_xml))

        self.output = """<study>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>12/01/20</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <Component_ID>1534436</Component_ID>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
<timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/><formImportedFieldName/><redcapFieldNameValue/><redcapFieldNameUnits/><redcapFieldNameStatus/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>12/01/20</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <Component_ID>1534435</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
<timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/><formImportedFieldName/><redcapFieldNameValue/><redcapFieldNameUnits/><redcapFieldNameStatus/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>04/18/19</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
<timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/><formImportedFieldName/><redcapFieldNameValue/><redcapFieldNameUnits/><redcapFieldNameStatus/></subject>
</study>
"""
        self.expect = etree.tostring(etree.fromstring(self.output))
        return()


    def test_add_elements_to_tree(self):

        redi.add_elements_to_tree(self.data_tree)

        self.result = etree.tostring(self.data_tree)
        self.assertEqual(self.expect, self.result)

    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
