import json
import unittest
import tempfile
import os
import sys

from lxml import etree

sys.path.append('bin/')
import redi

class TestUpdateRedcapForm(unittest.TestCase):

    def setUp(self):
        self.rawXml = """<?xml version='1.0' encoding='US-ASCII'?>
<study>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>04/17/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <COMPONENT_ID>1534436</COMPONENT_ID>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>04/17/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <COMPONENT_ID>1534435</COMPONENT_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>09/12/22</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <COMPONENT_ID>1558221</COMPONENT_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/></subject>
</study>
"""
        self.data = etree.ElementTree(etree.fromstring(self.rawXml))

        self.translationTable = """<rediFieldMap>
    <clinicalComponent>
        <clinicalComponentId>1534435</clinicalComponentId>
        <clinicalComponentName>HEMOGLOBIN</clinicalComponentName>
        <redcapFormName>cbc</redcapFormName>
        <redcapFieldNameValue>hemo_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Hemoglobin</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Hemoglobin units</redcapFieldNameUnitsDescriptiveText>
        <lbtest>hemo_lbtest</lbtest>
        <lbtestcd>hemo_lbtestcd</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>1558221</clinicalComponentId>
        <clinicalComponentName>BILIRUBIN DIRECT</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>dbil_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Direct Bilirubin</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>dbil_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Direct Bilirubin units</redcapFieldNameUnitsDescriptiveText>
        <lbtest>Total Bilirubin</lbtest>
        <lbtestcd>BILI</lbtestcd>
    </clinicalComponent>
</rediFieldMap>
"""

        self.translationTableTree = etree.ElementTree(etree.fromstring(self.translationTable))

        self.output = """<?xml version='1.0' encoding='US-ASCII'?>
<study>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>04/17/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <COMPONENT_ID>1534436</COMPONENT_ID>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp/><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>04/17/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <COMPONENT_ID>1534435</COMPONENT_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>09/12/22</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <COMPONENT_ID>1558221</COMPONENT_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp/><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/></subject>
</study>
"""
        self.expect = etree.tostring(etree.fromstring(self.output))
        return()


    def test_updateRedcapForm(self):
        redi.update_redcap_form(self.data, self.translationTableTree, 'undefined')
        result = etree.tostring(self.data)
        self.assertEqual(self.expect, result)


    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
