'''
@author : Mohan
email : mohan88@ufl.edu

This file tests for the function parse_translation_table

'''
import unittest
import os
from lxml import etree
import redi

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestParseTranslationTable(unittest.TestCase):

    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        self.sampleData = """<rediFieldMap>
    <clinicalComponent>
        <clinicalComponentId>123456</clinicalComponentId>
        <clinicalComponentName>TestComponent</clinicalComponentName>
        <redcapFormName>Test</redcapFormName>
        <redcapFieldNameValue>TestField1</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>TestField</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>TestField1Units</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>TestFieldUnits_Description</redcapFieldNameUnitsDescriptiveText>
        <redcapStatusFieldName>TestFieldStatus</redcapStatusFieldName>
        <lbtest>dummytest</lbtest>
        <lbtestcd>dummytest</lbtestcd>
    </clinicalComponent>
    </rediFieldMap>
"""
        
    def test_parse_translation_table(self):
        file_name = "tempFile.xml"
        temp_xml = open(file_name, "wb")
        temp_xml.write(self.sampleData)
        temp_xml.close()
        result = redi.parse_raw_xml('tempFile.xml')
        result_str = etree.tostring(result, method='xml', pretty_print=True)
        self.assertEqual(self.sampleData, result_str)
        os.remove(file_name)
    
    def test_parse_raw_xml_without_file(self):
        self.assertRaises(redi.LogException,redi.parse_raw_xml,'')  
        
    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
