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


class TestUpdateRedcapFieldNameValueAndUnits(unittest.TestCase):

    def setUp(self):
        self.raw_xml = """<study>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>10/01/17</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
<timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/><redcapFieldNameValue/><redcapFieldNameUnits/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>10/01/17</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
<timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/><redcapFieldNameValue/><redcapFieldNameUnits/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>05/05/22</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
<timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/><redcapFieldNameValue/><redcapFieldNameUnits/></subject>
</study>
"""
        self.data_tree = etree.ElementTree(etree.fromstring(self.raw_xml))

        self.lookup_table = """<rediFieldMap>
    <clinicalComponent>
        <loinc_code>1534435</loinc_code>
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
        <loinc_code>1558221</loinc_code>
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


        self.lookup_table_tree = etree.ElementTree(etree.fromstring(self.lookup_table))

        self.output = """<study>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>10/01/17</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <loinc_code>1534436</loinc_code>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
<timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/><redcapFieldNameValue>undefined</redcapFieldNameValue><redcapFieldNameUnits>redcapFieldNameUnitsUndefined</redcapFieldNameUnits></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>10/01/17</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <loinc_code>1534435</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
<timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>05/05/22</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <loinc_code>1558221</loinc_code>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
<timestamp/><redcapFormName/><eventName/><formDateField/><formCompletedFieldName/><redcapFieldNameValue>dbil_lborres</redcapFieldNameValue><redcapFieldNameUnits>dbil_lborresu</redcapFieldNameUnits></subject>
</study>
"""
        self.expect = etree.tostring(etree.fromstring(self.output))
        return()


    def test_update_redcap_field_name_value_and_units(self):
        redi.update_redcap_field_name_value_and_units(self.data_tree, self.lookup_table_tree, 'undefined')
        self.result = etree.tostring(self.data_tree)
        self.assertEqual(self.expect, self.result)

    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
