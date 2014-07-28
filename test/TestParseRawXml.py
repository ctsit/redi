'''
@author : Mohan
email : mohan88@ufl.edu

This file tests for the function parse_raw_xml

'''
import unittest
import os
import sys
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root + 'bin/')
from lxml import etree
import redi


class TestParseRawXml(unittest.TestCase):

    def setUp(self):
        redi.configure_logging()
        self.sampleData = """<study>
        <subject>
            <NAME>TestSubject1</NAME>
            <COMPONENT_ID>test1</COMPONENT_ID>
            <ORD_VALUE>0.12</ORD_VALUE>
            <REFERENCE_LOW>0.34</REFERENCE_LOW>
            <REFERENCE_HIGH>5.60</REFERENCE_HIGH>
            <REFERENCE_UNIT>mIU/L</REFERENCE_UNIT>
            <SPECIMN_TAKEN_TIME>7891-11-30 11:12:00</SPECIMN_TAKEN_TIME>
            <RESULT_DATE>1934-12-29 00:00:00</RESULT_DATE>
            <STUDY_ID>1234-5678</STUDY_ID>
        </subject>
        <subject>
            <NAME>TestSubject2</NAME>
            <COMPONENT_ID>test2</COMPONENT_ID>
            <ORD_VALUE>8.7</ORD_VALUE>
            <REFERENCE_LOW/>
            <REFERENCE_HIGH/>
            <REFERENCE_UNIT>ml</REFERENCE_UNIT>
            <SPECIMN_TAKEN_TIME>1909-8-27 16:13:00</SPECIMN_TAKEN_TIME>
            <RESULT_DATE>1904-12-28 00:00:00</RESULT_DATE>
            <STUDY_ID>987-654</STUDY_ID>
        </subject>
    </study>
"""
        
    def test_parse_raw_xml_with_file(self):
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
